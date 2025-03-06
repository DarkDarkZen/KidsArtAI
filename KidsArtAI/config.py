import os
import sys

# Получение токена бота из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    print("Ошибка: Переменная окружения BOT_TOKEN не установлена.")
    print("Установите переменную окружения BOT_TOKEN с вашим токеном Telegram бота.")
    print("Пример: export BOT_TOKEN='your_telegram_bot_token'")
    sys.exit(1)

# Получение API-ключа OpenAI из переменных окружения
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("Предупреждение: Переменная окружения OPENAI_API_KEY не установлена.")
    print("Некоторые функции, связанные с OpenAI, могут быть недоступны.")
    # Не завершаем работу, так как это может быть не критично на начальном этапе 