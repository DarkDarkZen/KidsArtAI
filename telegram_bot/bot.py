from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram_bot import handlers
import os
from config import BOT_TOKEN


def run_bot():
    # Создаем экземпляр приложения бота
    # Получаем токен из переменных окружения или из config.py
    token = os.environ.get('BOT_TOKEN', BOT_TOKEN)
    
    if token == 'YOUR_BOT_TOKEN':
        raise ValueError("Пожалуйста, установите правильный токен бота в переменной окружения BOT_TOKEN или в файле config.py")
    
    application = Application.builder().token(token).build()
    
    # Регистрируем обработчики команд
    application.add_handler(CommandHandler('start', handlers.start))
    application.add_handler(CommandHandler('help', handlers.help_command))
    application.add_handler(CommandHandler('report', handlers.report))
    application.add_handler(CommandHandler('clear_history', handlers.clear_history))
    
    # Регистрируем обработчик для обычных сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.handle_text))
    
    # Запуск бота в режиме polling
    application.run_polling() 