import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Получение токена бота из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    logger.error("Переменная окружения BOT_TOKEN не установлена")
    exit(1)

# URL для Telegram Mini App
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://kidsartai-production.up.railway.app")
logger.info(f"Используется URL для Telegram Mini App: {WEBAPP_URL}")

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет сообщение с кнопкой для запуска Telegram Mini App."""
    user = update.effective_user
    logger.info(f"Пользователь {user.id} запустил команду /start")
    
    # Создаем кнопку для запуска веб-приложения
    keyboard = [
        [InlineKeyboardButton(
            "🎨 Analyze Child's Drawing", 
            web_app=WebAppInfo(url=WEBAPP_URL)
        )]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"Привет, {user.first_name}! Нажмите на кнопку ниже, чтобы запустить приложение:",
        reply_markup=reply_markup
    )

# Обработчик команды /webapp
async def webapp(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет кнопку для запуска Telegram Mini App."""
    logger.info(f"Пользователь {update.effective_user.id} запустил команду /webapp")
    
    # Создаем кнопку для запуска веб-приложения
    keyboard = [
        [InlineKeyboardButton(
            "🎨 Запустить приложение", 
            web_app=WebAppInfo(url=WEBAPP_URL)
        )]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Нажмите на кнопку ниже, чтобы запустить приложение:",
        reply_markup=reply_markup
    )

# Обработчик для текстовых сообщений
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Эхо-ответ на сообщение пользователя."""
    logger.info(f"Пользователь {update.effective_user.id} отправил сообщение: {update.message.text}")
    await update.message.reply_text(f"Вы сказали: {update.message.text}")

def main() -> None:
    """Запускает бота."""
    logger.info("Запуск бота")
    
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()

    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("webapp", webapp))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Запускаем бота
    logger.info("Бот запущен")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main() 