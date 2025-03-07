import asyncio
from telegram.ext import Application
from telegram import Update, BotCommand
from config import BOT_TOKEN
from handlers import group_bot, user_history_bot, ai_stream, mini_app
from utils.logger import setup_logging

async def setup_commands(app):
    """Настройка команд бота, которые будут отображаться в меню."""
    commands = [
        BotCommand("start", "Запустить бота и показать кнопку анализа"),
        BotCommand("analyze", "Анализировать детский рисунок"),
        BotCommand("help", "Показать справку по командам"),
        BotCommand("history", "Показать историю сообщений")
    ]
    await app.bot.set_my_commands(commands)

def main():
    setup_logging()  # Инициализация логирования

    # Инициализация приложения Telegram bot
    app = Application.builder().token(BOT_TOKEN).build()

    # Настройка команд бота
    asyncio.run(setup_commands(app))

    # Регистрация обработчика для Telegram Mini App
    mini_app.setup_handlers(app)
    
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