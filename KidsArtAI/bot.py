import asyncio
from telegram.ext import Application
from telegram import Update, BotCommand, MenuButtonWebApp, WebAppInfo
from config import BOT_TOKEN, WEBAPP_URL
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
    
    # Настройка кнопки меню для Telegram Mini App
    await app.bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(text="Analyze Drawing", web_app=WebAppInfo(url=WEBAPP_URL))
    )
    print(f"Настроена кнопка меню для Telegram Mini App: {WEBAPP_URL}")

def main():
    setup_logging()  # Инициализация логирования

    # Инициализация приложения Telegram bot
    app = Application.builder().token(BOT_TOKEN).build()

    # Настройка команд бота и кнопки меню
    asyncio.run(setup_commands(app))

    # Регистрация обработчика для Telegram Mini App
    # Этот обработчик должен быть зарегистрирован первым, чтобы иметь приоритет
    mini_app.setup_handlers(app)
    
    # Регистрация остальных обработчиков
    # Эти обработчики будут иметь более низкий приоритет
    ai_stream.setup_handlers(app)
    group_bot.setup_handlers(app)
    user_history_bot.setup_handlers(app)

    # Запуск бота в режиме polling
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main() 