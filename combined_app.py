import asyncio
import logging
import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Получение токена бота из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    logger.error("Переменная окружения BOT_TOKEN не установлена")
    exit(1)
else:
    # Выводим первые и последние 5 символов токена для диагностики
    token_preview = f"{BOT_TOKEN[:5]}...{BOT_TOKEN[-5:]}"
    logger.info(f"Токен бота загружен успешно: {token_preview}")

# URL для Telegram Mini App
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://kidsartai-production.up.railway.app")
logger.info(f"Используется URL для Telegram Mini App: {WEBAPP_URL}")

# Создаем FastAPI приложение
app = FastAPI()

# Подключение статических файлов
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web/static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
    logger.info(f"Статические файлы подключены из директории: {static_dir}")

# Инициализация шаблонов
templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web/templates")
templates = Jinja2Templates(directory=templates_dir)
logger.info(f"Шаблоны инициализированы из директории: {templates_dir}")

# Глобальная переменная для хранения экземпляра бота
bot_app = None

@app.get("/health")
async def health_check():
    bot_status = "running" if bot_app and bot_app.is_running else "not running"
    return JSONResponse({
        "status": "healthy", 
        "bot_token_preview": f"{BOT_TOKEN[:5]}...{BOT_TOKEN[-5:]}", 
        "bot_status": bot_status
    })

@app.get("/")
async def index(request: Request):
    # Рендерим главный UI экран Telegram mini app
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/railway")
async def railway_root():
    bot_status = "running" if bot_app and bot_app.is_running else "not running"
    return JSONResponse({
        "status": "DrawingMind is running", 
        "version": "1.0.0",
        "environment": os.environ.get("RAILWAY_ENVIRONMENT", "unknown"),
        "bot_token_preview": f"{BOT_TOKEN[:5]}...{BOT_TOKEN[-5:]}",
        "bot_status": bot_status
    })

# Обработчик команды /start для Telegram бота
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет сообщение с кнопкой для запуска Telegram Mini App."""
    user = update.effective_user
    logger.info(f"Пользователь {user.id} запустил команду /start")
    
    # Создаем кнопку для запуска веб-приложения
    keyboard = [
        [InlineKeyboardButton(
            "🎨 Analyze Child's Drawing", 
            web_app=WebAppInfo(url=WEBAPP_URL)
        )]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"Привет, {user.first_name}! Нажмите на кнопку ниже, чтобы запустить приложение:",
        reply_markup=reply_markup
    )

# Обработчик команды /webapp для Telegram бота
async def webapp(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет кнопку для запуска Telegram Mini App."""
    logger.info(f"Пользователь {update.effective_user.id} запустил команду /webapp")
    
    # Создаем кнопку для запуска веб-приложения
    keyboard = [
        [InlineKeyboardButton(
            "🎨 Запустить приложение", 
            web_app=WebAppInfo(url=WEBAPP_URL)
        )]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Нажмите на кнопку ниже, чтобы запустить приложение:",
        reply_markup=reply_markup
    )

# Обработчик для текстовых сообщений в Telegram боте
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Эхо-ответ на сообщение пользователя."""
    logger.info(f"Пользователь {update.effective_user.id} отправил сообщение: {update.message.text}")
    await update.message.reply_text(f"Вы сказали: {update.message.text}")

async def run_bot():
    """Запускает Telegram бота."""
    global bot_app
    logger.info("Инициализация бота")
    
    try:
        # Создаем приложение
        bot_app = Application.builder().token(BOT_TOKEN).build()

        # Регистрируем обработчики
        bot_app.add_handler(CommandHandler("start", start))
        bot_app.add_handler(CommandHandler("webapp", webapp))
        bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

        # Запускаем бота
        logger.info("Запуск бота...")
        await bot_app.initialize()
        await bot_app.start()
        logger.info("Бот успешно запущен")
        
        # Запускаем polling в бесконечном цикле
        async with bot_app:
            logger.info("Запуск polling...")
            await bot_app.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {str(e)}")
        raise

async def run_web():
    """Запускает веб-сервер."""
    config = uvicorn.Config(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    """Запускает и веб-сервер, и бота."""
    logger.info("Запуск приложения")
    
    # Запускаем бота и веб-сервер параллельно
    await asyncio.gather(
        run_bot(),
        run_web()
    )

if __name__ == "__main__":
    # Запускаем все асинхронно
    asyncio.run(main()) 