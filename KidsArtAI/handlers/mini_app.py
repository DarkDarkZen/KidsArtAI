from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import CommandHandler, CallbackQueryHandler, ContextTypes, filters
from config import WEBAPP_URL
import logging

# Получаем логгер
logger = logging.getLogger(__name__)

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start с кнопкой для запуска Telegram Mini App."""
    logger.info(f"Вызван обработчик cmd_start в mini_app.py для пользователя {update.effective_user.id}")
    
    user = update.effective_user
    
    # Создаем кнопку для запуска веб-приложения
    keyboard = [
        [InlineKeyboardButton(
            "🎨 Analyze Child's Drawing", 
            web_app=WebAppInfo(url=WEBAPP_URL)
        )]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        await update.message.reply_text(
            f"👋 Привет, {user.first_name}!\n\n"
            "Я бот для анализа детских рисунков DrawingMind.\n\n"
            "Нажмите на кнопку ниже, чтобы загрузить и проанализировать рисунок:",
            reply_markup=reply_markup
        )
        logger.info(f"Отправлено сообщение с кнопкой для пользователя {user.id}")
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения: {str(e)}")
    
    # Возвращаем True, чтобы остановить обработку другими обработчиками
    return True

async def cmd_analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /analyze для запуска Telegram Mini App."""
    logger.info(f"Вызван обработчик cmd_analyze в mini_app.py для пользователя {update.effective_user.id}")
    
    # Создаем кнопку для запуска веб-приложения
    keyboard = [
        [InlineKeyboardButton(
            "🎨 Analyze Child's Drawing", 
            web_app=WebAppInfo(url=WEBAPP_URL)
        )]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        await update.message.reply_text(
            "Нажмите на кнопку ниже, чтобы загрузить и проанализировать рисунок:",
            reply_markup=reply_markup
        )
        logger.info(f"Отправлено сообщение с кнопкой для пользователя {update.effective_user.id}")
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения: {str(e)}")
    
    # Возвращаем True, чтобы остановить обработку другими обработчиками
    return True

def setup_handlers(app):
    """Регистрация обработчиков для Telegram Mini App."""
    logger.info("Регистрация обработчиков для Telegram Mini App")
    
    # Удаляем все существующие обработчики команды /start
    app.handlers.clear()
    logger.info("Все существующие обработчики удалены")
    
    # Используем группу 0 для высокого приоритета (меньшее число = выше приоритет)
    app.add_handler(CommandHandler("start", cmd_start, filters=filters.ChatType.PRIVATE), group=0)
    app.add_handler(CommandHandler("analyze", cmd_analyze, filters=filters.ChatType.PRIVATE), group=0)
    
    logger.info("Обработчики для Telegram Mini App зарегистрированы") 