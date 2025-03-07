from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import CommandHandler, CallbackQueryHandler, ContextTypes
from config import WEBAPP_URL

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start с кнопкой для запуска Telegram Mini App."""
    user = update.effective_user
    
    # Создаем кнопку для запуска веб-приложения
    keyboard = [
        [InlineKeyboardButton(
            "🎨 Analyze Child's Drawing", 
            web_app=WebAppInfo(url=WEBAPP_URL)
        )]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"👋 Привет, {user.first_name}!\n\n"
        "Я бот для анализа детских рисунков DrawingMind.\n\n"
        "Нажмите на кнопку ниже, чтобы загрузить и проанализировать рисунок:",
        reply_markup=reply_markup
    )

async def cmd_analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /analyze для запуска Telegram Mini App."""
    # Создаем кнопку для запуска веб-приложения
    keyboard = [
        [InlineKeyboardButton(
            "🎨 Analyze Child's Drawing", 
            web_app=WebAppInfo(url=WEBAPP_URL)
        )]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Нажмите на кнопку ниже, чтобы загрузить и проанализировать рисунок:",
        reply_markup=reply_markup
    )

def setup_handlers(app):
    """Регистрация обработчиков для Telegram Mini App."""
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("analyze", cmd_analyze)) 