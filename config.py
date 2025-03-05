import os

# Токен бота – рекомендуется установить через переменные окружения
BOT_TOKEN = os.environ.get('BOT_TOKEN', 'YOUR_BOT_TOKEN')

# URL подключения к базе данных (например, для хранения истории сообщений)
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///user_history.db') 