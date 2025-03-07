import asyncio
from telegram.ext import Application, CommandHandler, filters
from telegram import Update, BotCommand, MenuButtonWebApp, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from config import BOT_TOKEN, WEBAPP_URL
from handlers import group_bot, user_history_bot, ai_stream, mini_app
from utils.logger import setup_logging

# Глобальный логгер
logger = None

async def setup_commands(app):
    """Настройка команд бота, которые будут отображаться в меню."""
    logger.info("Настройка команд бота")
    
    commands = [
        BotCommand("start", "Запустить бота и показать кнопку анализа"),
        BotCommand("analyze", "Анализировать детский рисунок"),
        BotCommand("help", "Показать справку по командам"),
        BotCommand("history", "Показать историю сообщений")
    ]
    
    try:
        await app.bot.set_my_commands(commands)
        logger.info("Команды бота настроены успешно")
    except Exception as e:
        logger.error(f"Ошибка при настройке команд бота: {str(e)}")
    
    # Настройка кнопки меню для Telegram Mini App
    try:
        await app.bot.set_chat_menu_button(
            menu_button=MenuButtonWebApp(text="Analyze Drawing", web_app=WebAppInfo(url=WEBAPP_URL))
        )
        logger.info(f"Настроена кнопка меню для Telegram Mini App: {WEBAPP_URL}")
    except Exception as e:
        logger.error(f"Ошибка при настройке кнопки меню: {str(e)}")

async def test_command(update: Update, context):
    """Тестовая команда для проверки работы бота."""
    logger.info(f"Вызвана тестовая команда от пользователя {update.effective_user.id}")
    await update.message.reply_text("Тестовая команда работает!")

async def direct_start_command(update: Update, context):
    """Прямой обработчик команды /start с кнопкой для запуска Telegram Mini App."""
    logger.info(f"Вызван прямой обработчик команды /start для пользователя {update.effective_user.id}")
    
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

def main():
    global logger
    # Инициализация логирования
    logger = setup_logging()
    logger.info("Запуск бота")

    try:
        # Инициализация приложения Telegram bot
        app = Application.builder().token(BOT_TOKEN).build()
        logger.info("Приложение Telegram bot инициализировано")

        # Настройка команд бота и кнопки меню
        asyncio.run(setup_commands(app))

        # Добавляем прямой обработчик команды /start
        app.add_handler(CommandHandler("start", direct_start_command, filters=filters.ChatType.PRIVATE))
        logger.info("Прямой обработчик команды /start зарегистрирован")

        # Добавляем тестовую команду
        app.add_handler(CommandHandler("test", test_command))
        logger.info("Тестовая команда зарегистрирована")

        # Регистрация остальных обработчиков
        # Эти обработчики будут иметь более низкий приоритет
        ai_stream.setup_handlers(app)
        logger.info("Обработчики ai_stream зарегистрированы")
        
        group_bot.setup_handlers(app)
        logger.info("Обработчики group_bot зарегистрированы")
        
        user_history_bot.setup_handlers(app)
        logger.info("Обработчики user_history_bot зарегистрированы")

        # Запуск бота в режиме polling
        logger.info("Запуск бота в режиме polling")
        app.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {str(e)}")

if __name__ == "__main__":
    main() 