# Project Overview
GPT Telegram mini app для анализа детских рисунков с целью оценки психологического состояния и развития ребенка. Приложение должно обрабатывать загруженные изображения и предоставлять подробный отчет. И поддерживать threads и streaming mode.

# Core Functionalities
## 1. Bot should be deployed on railway.app and should work in polling mode
## 2. Bot should support openai streaming mode
## 3. Bot can be added into telegram groups
## 4. Bot should support threads (user id's and can store user message hystory)
## 5. Интерфейс бота
### 5.1. Реализовать двуязычный интерфейс (русский и английский).
### 5.2. Обеспечить возможность переключения языка в любой момент.
### 5.3. Создать интуитивно понятный дизайн, соответствующий стилистике Telegram.
## 6. Загрузка изображений
### 6.1. Поддержка загрузки изображений в различных форматах, включая HEIC.
### 6.2. Возможность сделать фото рисунка непосредственно в приложении.
## 7. Реализовать алгоритм анализа рисунков, оценивающий следующие параметры:
### 7.1. Психологический возраст.
### 7.2. Уровень развития воображения и интеллекта.
### 7.3. Эмоциональный интеллект.
### 7.4. Умственное и эмоциональное развитие.
### 7.5. Физическое и психологическое состояние.
## 8. Формирование отчета
### 8.1. Генерировать подробный отчет на основе анализа рисунка.
### 8.2. Включить рекомендацию о необходимости анализа нескольких рисунков для более точных выводов.
### 8.3. Предоставить возможность сохранения и отправки отчета.
## 9. Система оплаты
### 9.1. Интегрировать систему оплаты со следующими тарифами:
####  - 100 рублей за анализ 1 рисунка.
####  - 1000 рублей за месяц использования.
####  - 10000 рублей за год использования.
### 9.2. Обеспечить поддержку оплаты российскими банковскими картами.
### 9.3. Предоставить возможность бесплатного анализа первого рисунка.
## 10. Рабочий процесс
### 10.1. Пользователь открывает Telegram Mini App и загружает рисунок (поддержка в том числе HEIC формата) или делает фото рисунка (первый анализ бесплатный).
### 10.2. Приложение обрабатывает изображение и формирует отчет.
### 10.3. Для последующих анализов пользователь выбирает тариф или вводит промо-код.
### 10.4. После оплаты пользователь получает отчет.
## 11. There should be an option to clear message history for a user.
## 12. validation for user inputs.
## 13. confirmation dialogs for critical settings changes.
## 14. Implement settings export/import functionality.
## 15. Implement all needed logging and debugging into the code base, so it could be easily turned off after the project is perfectly running in production and turned back on when it is necessairy to troubleshoot possible issues.
## 16. Create a compehensible README.md file in Russian for this project.

# Documentation
## Example of Procfile for Railway:
```
worker: python bot.py

```

## Example of Railway configuration file:
```
{
    "$schema": "https://railway.app/railway.schema.json",
    "build": {
        "builder": "NIXPACKS"
    },
    "deploy": {
        "startCommand": "python bot.py",
        "restartPolicyType": "ON_FAILURE",
        "restartPolicyMaxRetries": 10
    }
}```

## Example of simple status endpoint for railway.app deployment
```
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/health")
async def health_check():
    return JSONResponse({"status": "healthy"})
```

## Example of support openai streaming mode
```
from telegram import Update
from telegram.ext import ContextTypes
from openai import AsyncOpenAI
import asyncio

async def stream_openai_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Initial response message
    response_message = await update.message.reply_text("⌛ Генерирую ответ...")
    collected_chunks = []
    
    try:
        client = AsyncOpenAI()
        # Start streaming response
        stream = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": update.message.text}],
            stream=True
        )
        
        async for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                collected_chunks.append(chunk.choices[0].delta.content)
                # Update message every 20 chunks or when chunk ends with sentence
                if len(collected_chunks) % 20 == 0 or chunk.choices[0].delta.content.endswith(('.', '!', '?')):
                    current_response = ''.join(collected_chunks)
                    try:
                        await response_message.edit_text(current_response)
                    except Exception:
                        continue
                        
        # Final update with complete response
        final_response = ''.join(collected_chunks)
        await response_message.edit_text(final_response)
        
    except Exception as e:
        await response_message.edit_text(f"❌ Произошла ошибка: {str(e)}")

# Register handler in your bot
async def setup_handlers(application):
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, stream_openai_response))
```
## Example of a Telegram bot that can work in groups with proper permission handling and group-specific features.
```
from telegram import Update, ChatMemberUpdated, ChatPermissions, ChatMember
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ChatMemberHandler,
    ContextTypes,
    filters
)
from typing import Optional, Tuple

class GroupBot:
    def __init__(self, token: str):
        self.application = Application.builder().token(token).build()
        self.setup_handlers()

    def setup_handlers(self):
        # Basic commands
        self.application.add_handler(CommandHandler("start", self.cmd_start))
        self.application.add_handler(CommandHandler("help", self.cmd_help))
        
        # Admin commands
        self.application.add_handler(CommandHandler("settings", self.cmd_settings))
        self.application.add_handler(CommandHandler("warn", self.cmd_warn))
        
        # Track member changes
        self.application.add_handler(ChatMemberHandler(self.track_members, ChatMemberHandler.CHAT_MEMBER))
        
        # Message handlers
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        if update.effective_chat.type == "private":
            await update.message.reply_text("Привет! Добавьте меня в группу для полного функционала.")
        else:
            await update.message.reply_text("Бот активирован в этой группе! Используйте /help для списка команд.")

    async def cmd_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = (
            "📋 Доступные команды:\n"
            "/settings - Настройки группы (только админы)\n"
            "/warn - Предупредить пользователя (только админы)\n"
            "/help - Показать это сообщение"
        )
        await update.message.reply_text(help_text)

    async def check_admin(self, update: Update) -> bool:
        """Check if user is admin"""
        user_id = update.effective_user.id
        chat_id = update.effective_chat.id
        
        member = await update.effective_chat.get_member(user_id)
        return member.status in ["creator", "administrator"]

    async def cmd_settings(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle group settings (admin only)"""
        if not await self.check_admin(update):
            await update.message.reply_text("⚠️ Эта команда доступна только администраторам.")
            return

        settings_text = (
            "⚙️ Настройки группы:\n"
            "1. Режим модерации: Включен\n"
            "2. Приветствие новых участников: Включено\n"
            "3. Антиспам: Включен"
        )
        await update.message.reply_text(settings_text)

    async def cmd_warn(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Warn user (admin only)"""
        if not await self.check_admin(update):
            await update.message.reply_text("⚠️ Эта команда доступна только администраторам.")
            return

        if not update.message.reply_to_message:
            await update.message.reply_text("↩️ Ответьте на сообщение пользователя, которого хотите предупредить.")
            return

        warned_user = update.message.reply_to_message.from_user
        await update.message.reply_text(f"⚠️ Пользователь {warned_user.mention_html()} получил предупреждение.")

    async def track_members(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Track member updates in the group"""
        result = self.extract_status_change(update.chat_member)
        if result is None:
            return

        was_member, is_member = result

        if not was_member and is_member:
            # New member joined
            await update.effective_chat.send_message(
                f"👋 Добро пожаловать, {update.chat_member.new_chat_member.member.mention_html()}!"
            )
        elif was_member and not is_member:
            # Member left
            await update.effective_chat.send_message(
                f"👋 До свидания, {update.chat_member.new_chat_member.member.mention_html()}!"
            )

    @staticmethod
    def extract_status_change(chat_member_update: ChatMemberUpdated) -> Optional[Tuple[bool, bool]]:
        """Extract status change from ChatMemberUpdated event"""
        status_change = chat_member_update.difference().get("status")
        if status_change is None:
            return None

        old_is_member = chat_member_update.old_chat_member.status in [
            ChatMember.MEMBER,
            ChatMember.OWNER,
            ChatMember.ADMINISTRATOR,
        ]
        new_is_member = chat_member_update.new_chat_member.status in [
            ChatMember.MEMBER,
            ChatMember.OWNER,
            ChatMember.ADMINISTRATOR,
        ]
        return old_is_member, new_is_member

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular messages"""
        # Example of basic message handling
        if update.effective_chat.type != "private":
            # Group message handling logic here
            pass

    def run(self):
        """Run the bot"""
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    BOT_TOKEN = "YOUR_BOT_TOKEN"
    bot = GroupBot(BOT_TOKEN)
    bot.run()
```

## Example of a Telegram bot that manages user IDs and message history using SQLite for storage.
```
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import sqlite3
from datetime import datetime
import json
from typing import Optional, List, Dict

class UserHistoryBot:
    def __init__(self, token: str, db_path: str = "user_history.db"):
        self.token = token
        self.db_path = db_path
        self.setup_database()
        self.application = Application.builder().token(token).build()
        self.setup_handlers()

    def setup_database(self):
        """Initialize SQLite database"""
        with sqlite3.connect(self.db_path) as conn:
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

    def setup_handlers(self):
        """Setup bot command and message handlers"""
        self.application.add_handler(CommandHandler("start", self.cmd_start))
        self.application.add_handler(CommandHandler("history", self.cmd_history))
        self.application.add_handler(CommandHandler("stats", self.cmd_stats))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

    async def save_user(self, user_data: Dict):
        """Save or update user information"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO users (user_id, username, first_name, last_name)
                VALUES (?, ?, ?, ?)
            """, (
                user_data['id'],
                user_data.get('username'),
                user_data.get('first_name'),
                user_data.get('last_name')
            ))

    async def save_message(self, user_id: int, message_text: str):
        """Save message to history"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO message_history (user_id, message_text)
                VALUES (?, ?)
            """, (user_id, message_text))

    async def get_user_history(self, user_id: int, limit: int = 10) -> List[Dict]:
        """Retrieve user message history"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT message_text, timestamp
                FROM message_history
                WHERE user_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            """, (user_id, limit))
            return [dict(row) for row in cursor.fetchall()]

    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        await self.save_user(user.to_dict())
        
        welcome_text = (
            f"👋 Здравствуйте, {user.first_name}!\n\n"
            "Доступные команды:\n"
            "/history - Показать историю сообщений\n"
            "/stats - Показать статистику\n"
        )
        await update.message.reply_text(welcome_text)

    async def cmd_history(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /history command"""
        user_id = update.effective_user.id
        history = await self.get_user_history(user_id)
        
        if not history:
            await update.message.reply_text("📭 История сообщений пуста")
            return

        history_text = "📋 Ваши последние сообщения:\n\n"
        for item in history:
            date = datetime.fromisoformat(item['timestamp']).strftime("%d.%m.%Y %H:%M")
            history_text += f"🕒 {date}\n📝 {item['message_text']}\n\n"
        
        await update.message.reply_text(history_text)

    async def cmd_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stats command"""
        user_id = update.effective_user.id
        
        with sqlite3.connect(self.db_path) as conn:
            # Get total messages count
            messages_count = conn.execute("""
                SELECT COUNT(*) FROM message_history WHERE user_id = ?
            """, (user_id,)).fetchone()[0]
            
            # Get first message date
            first_message = conn.execute("""
                SELECT MIN(timestamp) FROM message_history WHERE user_id = ?
            """, (user_id,)).fetchone()[0]

        stats_text = (
            "📊 Ваша статистика:\n\n"
            f"📝 Всего сообщений: {messages_count}\n"
            f"📅 Первое сообщение: {datetime.fromisoformat(first_message).strftime('%d.%m.%Y') if first_message else 'Нет данных'}"
        )
        
        await update.message.reply_text(stats_text)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular messages"""
        user = update.effective_user
        message_text = update.message.text
        
        # Save user data and message
        await self.save_user(user.to_dict())
        await self.save_message(user.id, message_text)
        
        # Optional: Acknowledge message receipt
        await update.message.reply_text("✅ Сообщение сохранено")

    def run(self):
        """Run the bot"""
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)
```

# Project File Structure
ChildrensDrawings/
├── Procfile                  // Файл для Railway, указывающий команду для запуска бота
├── railway.json              // Файл конфигурации для Railway deployment
├── requirements.txt          // Список зависимостей (все перечисленные библиотеки)
├── main.py                   // Главный файл, где запускается бот (обработка polling)
├── telegram_bot/             // Папка с логикой Telegram бота
│   ├── __init__.py
│   ├── handlers.py           // Файл для команд / сообщений (например, загрузка рисунка, команда start, report и т.д.)
│   ├── bot.py                // Конфигурация бота, настройка polling, подключение webhooks (если потребуется)
│   ├── utils.py              // Утилиты и вспомогательные функции (например, для работы с потоками)
│   └── payments.py           // Логика обработки платежей и тарифов
├── image_processing/         // Папка для логики анализа рисунков
│   ├── __init__.py
│   ├── analyzer.py           // Функции для обработки и анализа изображений
│   ├── models.py             // Модели или функции, использующие машинное обучение
│   └── report_generator.py   // Генерация отчетов на основе анализа
├── config.py                 // Конфигурационный файл с настройками проекта (токены, пути, параметры модели и т.д.)
├── logging_config.py         // Конфигурация логирования и отладки
└── README.md                 // Подробная документация проекта на русском языке
