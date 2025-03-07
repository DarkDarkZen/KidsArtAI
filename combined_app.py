import asyncio
import logging
import os
import sys
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логирования для корневого логгера
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

# Создаем форматтер
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Создаем обработчик для stdout
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(formatter)

# Очищаем существующие обработчики и добавляем новый
root_logger.handlers.clear()
root_logger.addHandler(stdout_handler)

# Настраиваем логгер для нашего приложения
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Отключаем передачу логов родительским логгерам
logger.propagate = False

# Добавляем тот же обработчик к логгеру приложения
logger.addHandler(stdout_handler)

# Настраиваем логгер для uvicorn
uvicorn_logger = logging.getLogger("uvicorn")
uvicorn_logger.handlers.clear()
uvicorn_logger.addHandler(stdout_handler)

logger.info("Инициализация приложения DrawingMind")

# Получение токена бота из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    logger.critical("Критическая ошибка: Переменная окружения BOT_TOKEN не установлена")
    sys.exit(1)
else:
    token_preview = f"{BOT_TOKEN[:5]}...{BOT_TOKEN[-5:]}"
    logger.info(f"Токен бота успешно загружен: {token_preview}")

# URL для Telegram Mini App
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://kidsartai-production.up.railway.app")
logger.info(f"URL для Telegram Mini App: {WEBAPP_URL}")

# Создаем FastAPI приложение
app = FastAPI(
    title="DrawingMind API",
    version="1.0.0",
    description="API для анализа детских рисунков"
)
logger.info("FastAPI приложение создано")

# Подключение статических файлов
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web/static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
    logger.info(f"Статические файлы подключены: {static_dir}")
else:
    logger.warning(f"Директория статических файлов не найдена: {static_dir}")

# Инициализация шаблонов
templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web/templates")
if os.path.exists(templates_dir):
    templates = Jinja2Templates(directory=templates_dir)
    logger.info(f"Шаблоны инициализированы: {templates_dir}")
else:
    logger.error(f"Директория шаблонов не найдена: {templates_dir}")
    raise FileNotFoundError(f"Директория шаблонов не найдена: {templates_dir}")

# Глобальные переменные для состояния приложения
bot_app = None
bot_task = None
startup_time = None

@app.get("/")
async def root():
    """Корневой эндпоинт"""
    logger.info("Получен запрос к корневому эндпоинту")
    return {"message": "DrawingMind API is running"}

@app.get("/health")
async def health_check():
    """Эндпоинт проверки состояния приложения"""
    global bot_app, bot_task, startup_time
    logger.info("Получен запрос к эндпоинту /health")
    try:
        bot_status = "running" if bot_app and bot_app.is_running else "not running"
        task_status = "running" if bot_task and not bot_task.done() else "not running"
        
        response = {
            "status": "healthy",
            "uptime": str(asyncio.get_event_loop().time() - startup_time) if startup_time else "unknown",
            "bot": {
                "status": bot_status,
                "token_preview": f"{BOT_TOKEN[:5]}...{BOT_TOKEN[-5:]}",
                "polling": task_status
            }
        }
        logger.info(f"Health check response: {response}")
        return JSONResponse(response)
    except Exception as e:
        error_msg = f"Ошибка при проверке состояния: {str(e)}"
        logger.error(error_msg)
        return JSONResponse(
            {"status": "unhealthy", "error": error_msg},
            status_code=500
        )

@app.get("/railway")
async def railway_root():
    """Эндпоинт информации о развертывании"""
    global bot_app, bot_task, startup_time
    logger.info("Получен запрос к эндпоинту /railway")
    try:
        bot_status = "running" if bot_app and bot_app.is_running else "not running"
        task_status = "running" if bot_task and not bot_task.done() else "not running"
        
        response = {
            "status": "DrawingMind is running",
            "version": "1.0.0",
            "environment": os.environ.get("RAILWAY_ENVIRONMENT", "unknown"),
            "uptime": str(asyncio.get_event_loop().time() - startup_time) if startup_time else "unknown",
            "bot": {
                "status": bot_status,
                "token_preview": f"{BOT_TOKEN[:5]}...{BOT_TOKEN[-5:]}",
                "polling": task_status
            }
        }
        logger.info(f"Railway status response: {response}")
        return JSONResponse(response)
    except Exception as e:
        error_msg = f"Ошибка при получении статуса Railway: {str(e)}"
        logger.error(error_msg)
        return JSONResponse(
            {"status": "error", "error": error_msg},
            status_code=500
        )

async def run_polling():
    """Запускает polling для Telegram бота"""
    global bot_app
    logger.info("Запуск polling для бота...")
    try:
        await bot_app.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        logger.error(f"Ошибка в процессе polling: {str(e)}")
        raise

@app.on_event("startup")
async def startup_event():
    """Запускает бота при старте FastAPI приложения"""
    global bot_app, bot_task, startup_time
    logger.info("Начало инициализации приложения")
    startup_time = asyncio.get_event_loop().time()
    
    try:
        # Создаем приложение бота
        bot_app = Application.builder().token(BOT_TOKEN).build()
        logger.info("Приложение бота создано")

        # Регистрируем обработчики
        bot_app.add_handler(CommandHandler("start", start))
        bot_app.add_handler(CommandHandler("webapp", webapp))
        bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
        logger.info("Обработчики команд зарегистрированы")

        # Инициализируем и запускаем бота
        await bot_app.initialize()
        await bot_app.start()
        logger.info("Бот успешно инициализирован и запущен")

        # Запускаем polling в отдельной задаче
        bot_task = asyncio.create_task(run_polling())
        logger.info("Задача polling запущена")
    except Exception as e:
        error_msg = f"Критическая ошибка при запуске бота: {str(e)}"
        logger.error(error_msg)
        if bot_app:
            await bot_app.shutdown()
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Останавливает бота при завершении работы приложения"""
    global bot_app, bot_task
    logger.info("Начало процесса остановки приложения")
    
    if bot_task:
        logger.info("Отмена задачи polling")
        bot_task.cancel()
        try:
            await bot_task
        except asyncio.CancelledError:
            logger.info("Задача polling успешно отменена")
        except Exception as e:
            logger.error(f"Ошибка при отмене задачи polling: {str(e)}")
    
    if bot_app:
        logger.info("Остановка бота")
        try:
            await bot_app.shutdown()
            logger.info("Бот успешно остановлен")
        except Exception as e:
            logger.error(f"Ошибка при остановке бота: {str(e)}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    logger.info(f"Запуск сервера на порту {port}")
    
    # Настройка конфигурации uvicorn
    config = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info",
        access_log=True,
        log_config=None  # Отключаем встроенную конфигурацию логирования
    )
    
    # Запуск сервера
    server = uvicorn.Server(config)
    server.run() 