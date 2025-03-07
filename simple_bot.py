import os
import logging
from telegram import Update
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

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет сообщение при получении команды /start."""
    user = update.effective_user
    logger.info(f"Пользователь {user.id} запустил команду /start")
    await update.message.reply_text(f'Привет, {user.first_name}! Я простой тестовый бот.')

# Обработчик команды /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет сообщение при получении команды /help."""
    logger.info(f"Пользователь {update.effective_user.id} запустил команду /help")
    await update.message.reply_text('Помощь!')

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
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Запускаем бота
    logger.info("Бот запущен")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main() 