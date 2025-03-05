FROM python:3.10-slim

WORKDIR /app

# Установка системных зависимостей для Pillow и других библиотек
RUN apt-get update && apt-get install -y \
    gcc \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# Копирование файлов проекта
COPY . .

# Установка зависимостей Python
RUN pip install --no-cache-dir -r requirements.txt

# Запуск бота
CMD ["python", "main.py"] 