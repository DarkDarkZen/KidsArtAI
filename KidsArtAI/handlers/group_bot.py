from telegram import Update, ChatMember, ChatMemberUpdated
from telegram.ext import CommandHandler, MessageHandler, ChatMemberHandler, ContextTypes, filters
from typing import Optional, Tuple

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды /start для групп и личных чатов."""
    if update.effective_chat.type == 'private':
        await update.message.reply_text("Привет! Добавьте меня в группу для полного функционала.")
    else:
        await update.message.reply_text("Бот активирован в этой группе! Используйте /help для списка команд.")

async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает справку по командам."""
    text = (
        "📋 Доступные команды:\n"
        "/settings - Настройки группы (только для администраторов)\n"
        "/warn - Предупредить пользователя (только для администраторов)\n"
        "/help - Справка по командам"
    )
    await update.message.reply_text(text)

async def check_admin(update: Update) -> bool:
    """Проверяет, является ли пользователь администратором."""
    user_id = update.effective_user.id
    chat = update.effective_chat
    member = await chat.get_member(user_id)
    return member.status in ["creator", "administrator"]

async def cmd_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды настроек группы."""
    if not await check_admin(update):
        await update.message.reply_text("⚠️ Эта команда доступна только администраторам.")
        return
    settings_text = (
        "⚙️ Настройки группы:\n"
        "1. Режим модерации: Включен\n"
        "2. Приветствие новых участников: Включено\n"
        "3. Антиспам: Включен"
    )
    await update.message.reply_text(settings_text)

async def cmd_warn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Предупреждение пользователя (администраторам)."""
    if not await check_admin(update):
        await update.message.reply_text("⚠️ Эта команда доступна только администраторам.")
        return
    if not update.message.reply_to_message:
        await update.message.reply_text("↩️ Ответьте на сообщение пользователя, которого хотите предупредить.")
        return
    warned_user = update.message.reply_to_message.from_user
    await update.message.reply_text(f"⚠️ Пользователь {warned_user.mention_html()} получил предупреждение.")

async def track_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка изменений статуса участников группы."""
    result = extract_status_change(update.chat_member)
    if result is None:
        return
    was_member, is_member = result
    if not was_member and is_member:
        await update.effective_chat.send_message(
            f"👋 Добро пожаловать, {update.chat_member.new_chat_member.member.mention_html()}!"
        )
    elif was_member and not is_member:
        await update.effective_chat.send_message(
            f"👋 До свидания, {update.chat_member.new_chat_member.member.mention_html()}!"
        )

def extract_status_change(chat_member_update: ChatMemberUpdated) -> Optional[Tuple[bool, bool]]:
    """Извлечение изменений статуса участника."""
    status_change = chat_member_update.difference().get("status")
    if status_change is None:
        return None
    old_is_member = chat_member_update.old_chat_member.status in [
        ChatMember.MEMBER, ChatMember.OWNER, ChatMember.ADMINISTRATOR
    ]
    new_is_member = chat_member_update.new_chat_member.status in [
        ChatMember.MEMBER, ChatMember.OWNER, ChatMember.ADMINISTRATOR
    ]
    return old_is_member, new_is_member

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка обычных сообщений в группах (при необходимости)."""
    # Логика обработки сообщений в группах может быть добавлена здесь.
    pass

def setup_handlers(app):
    """Регистрация команд и обработчиков для группового функционала."""
    # Используем группу 1 для более низкого приоритета
    app.add_handler(CommandHandler("start", cmd_start), group=1)
    app.add_handler(CommandHandler("help", cmd_help), group=1)
    app.add_handler(CommandHandler("settings", cmd_settings), group=1)
    app.add_handler(CommandHandler("warn", cmd_warn), group=1)
    app.add_handler(ChatMemberHandler(track_members, ChatMemberHandler.CHAT_MEMBER), group=1)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message), group=1) 