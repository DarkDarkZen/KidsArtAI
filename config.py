import os
import logging

# Настройка логирования
logger = logging.getLogger(__name__)

# Токен бота – рекомендуется установить через переменные окружения
# Для Railway.app: добавьте переменную окружения BOT_TOKEN в настройках проекта
# Для локальной разработки: замените 'YOUR_BOT_TOKEN' на ваш реальный токен
BOT_TOKEN = os.environ.get('BOT_TOKEN', '7654539187:AAFTBosgRopDeMEUbR7zUG5pdOCyhIhOlUA')

# URL подключения к базе данных (например, для хранения истории сообщений)
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///user_history.db') 