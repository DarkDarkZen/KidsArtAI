import logging
import os
import sys
from logging.handlers import RotatingFileHandler

def setup_logging():
    """Настройка логирования. В production логи можно отключать или перенаправлять."""
    # Создаем директорию для логов, если её нет
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Настраиваем корневой логгер
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    
    # Форматирование логов
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    # Обработчик для вывода в консоль
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # Обработчик для записи в файл
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, "bot.log"),
        maxBytes=10*1024*1024,  # 10 MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    
    # Логгер для библиотеки telegram
    telegram_logger = logging.getLogger("telegram")
    telegram_logger.setLevel(logging.INFO)
    
    # Логгер для нашего приложения
    app_logger = logging.getLogger("KidsArtAI")
    app_logger.setLevel(logging.DEBUG)
    
    # Выводим информацию о запуске
    app_logger.info("Логирование настроено")
    
    return app_logger 