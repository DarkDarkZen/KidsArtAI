from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram_bot import handlers


def run_bot():
    # Создаем экземпляр приложения бота
    application = Application.builder().token('YOUR_BOT_TOKEN').build()
    
    # Регистрируем обработчики команд
    application.add_handler(CommandHandler('start', handlers.start))
    application.add_handler(CommandHandler('help', handlers.help_command))
    application.add_handler(CommandHandler('report', handlers.report))
    application.add_handler(CommandHandler('clear_history', handlers.clear_history))
    
    # Регистрируем обработчик для обычных сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.handle_text))
    
    # Запуск бота в режиме polling
    application.run_polling() 