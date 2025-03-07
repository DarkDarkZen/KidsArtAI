import sqlite3
from datetime import datetime
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, ContextTypes, filters

DB_PATH = "user_history.db"

def setup_database():
    """Инициализация SQLite базы данных для хранения пользователей и истории сообщений."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS message_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                message_text TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        """)

async def save_user(user_data: dict):
    """Сохранение или обновление информации о пользователе."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT OR REPLACE INTO users (user_id, username, first_name, last_name)
            VALUES (?, ?, ?, ?)
        """, (
            user_data['id'],
            user_data.get('username'),
            user_data.get('first_name'),
            user_data.get('last_name')
        ))

async def save_message(user_id: int, message_text: str):
    """Сохранение сообщения в историю."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO message_history (user_id, message_text)
            VALUES (?, ?)
        """, (user_id, message_text))

async def get_user_history(user_id: int, limit: int = 10):
    """Получение истории сообщений пользователя."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute("""
            SELECT message_text, timestamp
            FROM message_history
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (user_id, limit))
        return [dict(row) for row in cursor.fetchall()]

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды /start для сохранения пользователя и приветствия."""
    user = update.effective_user
    await save_user(user.to_dict())
    text = (
        f"👋 Здравствуйте, {user.first_name}!\n\n"
        "Доступные команды:\n"
        "/history - Показать историю сообщений\n"
        "/stats - Показать статистику\n"
    )
    await update.message.reply_text(text)

async def cmd_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды /history для вывода истории сообщений."""
    user_id = update.effective_user.id
    history = await get_user_history(user_id)
    if not history:
        await update.message.reply_text("📭 История сообщений пуста")
        return
    text = "📋 Ваши последние сообщения:\n\n"
    for item in history:
        date = datetime.fromisoformat(item["timestamp"]).strftime("%d.%m.%Y %H:%M")
        text += f"🕒 {date}\n📝 {item['message_text']}\n\n"
    await update.message.reply_text(text)

async def cmd_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды /stats для показа статистики пользователя."""
    user_id = update.effective_user.id
    with sqlite3.connect(DB_PATH) as conn:
        messages_count = conn.execute("""
            SELECT COUNT(*) FROM message_history WHERE user_id = ?
        """, (user_id,)).fetchone()[0]
        first_message = conn.execute("""
            SELECT MIN(timestamp) FROM message_history WHERE user_id = ?
        """, (user_id,)).fetchone()[0]
    first_message_date = datetime.fromisoformat(first_message).strftime("%d.%m.%Y") if first_message else "Нет данных"
    text = (
        "📊 Ваша статистика:\n\n"
        f"📝 Всего сообщений: {messages_count}\n"
        f"📅 Первое сообщение: {first_message_date}"
    )
    await update.message.reply_text(text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Сохранение входящего текста как сообщения пользователя."""
    user = update.effective_user
    message_text = update.message.text
    await save_user(user.to_dict())
    await save_message(user.id, message_text)
    await update.message.reply_text("✅ Сообщение сохранено")

def setup_handlers(app):
    """Регистрация команд и обработчиков для истории сообщений."""
    setup_database()
    app.add_handler(CommandHandler("start", cmd_start), group=2)
    app.add_handler(CommandHandler("history", cmd_history), group=2)
    app.add_handler(CommandHandler("stats", cmd_stats), group=2)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message), group=2) 