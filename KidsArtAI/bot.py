import asyncio
from telegram.ext import Application
from telegram import Update
from config import BOT_TOKEN
from handlers import group_bot, user_history_bot, ai_stream
from utils.logger import setup_logging

def main():
    setup_logging()  # Инициализация логирования

    # Инициализация приложения Telegram bot
    app = Application.builder().token(BOT_TOKEN).build()

    # Регистрация обработчиков для группового режима
    group_bot.setup_handlers(app)
    # Регистрация обработчиков для управления историей сообщений
    user_history_bot.setup_handlers(app)
    # Регистрация обработчика для OpenAI streaming
    ai_stream.setup_handlers(app)

    # Запуск бота в режиме polling
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main() 