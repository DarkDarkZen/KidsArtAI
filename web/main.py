from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()

# Подключение статических файлов
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Инициализация шаблонов
templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
templates = Jinja2Templates(directory=templates_dir)

@app.get("/health")
async def health_check():
    return JSONResponse({"status": "healthy"})

@app.get("/")
async def index(request: Request):
    # Рендерим главный UI экран Telegram mini app
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/railway")
async def railway_root():
    return JSONResponse({
        "status": "KidsArtAI is running", 
        "version": "1.0.0",
        "environment": os.environ.get("RAILWAY_ENVIRONMENT", "unknown")
    })

if __name__ == "__main__":
    import uvicorn
    # Получаем порт из переменной окружения или используем 8080 по умолчанию
    port = int(os.environ.get("PORT", 8080))
    print(f"Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)