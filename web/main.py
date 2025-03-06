from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Подключение статических файлов
app.mount("/static", StaticFiles(directory="web/static"), name="static")

# Инициализация шаблонов (templates расположены в каталоге web/templates)
templates = Jinja2Templates(directory="web/templates")

@app.get("/health")
async def health_check():
    return JSONResponse({"status": "healthy"})

@app.get("/")
async def index(request: Request):
    # Рендерим главный UI экран Telegram mini app
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)