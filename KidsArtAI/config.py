import os
import sys

# Получение токена бота из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    print("Ошибка: Переменная окружения BOT_TOKEN не установлена.")
    print("Установите переменную окружения BOT_TOKEN с вашим токеном Telegram бота.")
    print("Пример: export BOT_TOKEN='your_telegram_bot_token'")
    sys.exit(1)
else:
    # Выводим первые и последние 5 символов токена для диагностики
    token_preview = f"{BOT_TOKEN[:5]}...{BOT_TOKEN[-5:]}"
    print(f"Токен бота загружен успешно: {token_preview}")
    
    # Проверяем формат токена (должен содержать двоеточие)
    if ":" not in BOT_TOKEN:
        print("Предупреждение: Формат токена бота может быть неправильным. Токен должен содержать двоеточие.")

# Получение API-ключа OpenAI из переменных окружения
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("Предупреждение: Переменная окружения OPENAI_API_KEY не установлена.")
    print("Некоторые функции, связанные с OpenAI, могут быть недоступны.")
    # Не завершаем работу, так как это может быть не критично на начальном этапе

# URL для Telegram Mini App
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://kidsartai-production.up.railway.app")
print(f"Используется URL для Telegram Mini App: {WEBAPP_URL}") 