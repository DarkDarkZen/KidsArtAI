from fastapi import FastAPI, Request, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import os
import aiofiles
import uuid
from datetime import datetime
import sys
import base64  # Добавляем импорт base64 для кодирования изображений

# Инициализация OpenAI API ключа из переменной окружения
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Инициализация OpenAI клиента, если ключ доступен
from openai import AsyncOpenAI
client = None
if OPENAI_API_KEY:
    client = AsyncOpenAI(api_key=OPENAI_API_KEY)

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене лучше указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение статических файлов
app.mount("/static", StaticFiles(directory="web/static"), name="static")

# Инициализация шаблонов
templates = Jinja2Templates(directory="web/templates")

# Создаем директорию для загруженных изображений, если её нет
UPLOAD_DIR = "web/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/health")
async def health_check():
    return JSONResponse({"status": "healthy"})

@app.get("/")
async def index(request: Request):
    # Рендерим главный UI экран Telegram mini app
    return templates.TemplateResponse("index.html", {"request": request})

# Добавляем обработчик корневого пути для Railway
@app.get("/railway")
async def railway_root():
    return JSONResponse({"status": "KidsArtAI is running", "version": "1.0.0"})

@app.post("/api/analyze")
async def analyze_drawing(image: UploadFile = File(...), language: str = Form("ru")):
    """
    API-эндпоинт для анализа детского рисунка с использованием OpenAI.
    """
    # Проверяем, инициализирован ли клиент OpenAI
    if not client:
        raise HTTPException(status_code=503, detail="OpenAI API не настроен. Проверьте переменную окружения OPENAI_API_KEY.")
        
    try:
        # Проверка типа файла
        if not image.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Файл должен быть изображением")
        
        # Генерируем уникальное имя файла
        file_extension = os.path.splitext(image.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        # Сохраняем загруженный файл
        async with aiofiles.open(file_path, "wb") as out_file:
            content = await image.read()
            await out_file.write(content)
        
        # Формируем промпт для OpenAI в зависимости от выбранного языка
        if language == "ru":
            prompt = """
            Проанализируй этот детский рисунок и предоставь краткую интерпретацию (не более абзаца) по каждому из следующих пунктов:
            1. Психологический возраст ребенка
            2. Уровень развития воображения и интеллекта
            3. Эмоциональный интеллект
            4. Уровень умственного и эмоционального развития
            5. Физическое и психологическое состояние
            
            Также дай конкретные рекомендации родителям:
            - Как поговорить с ребёнком о возможных проблемах
            - Как развивать выявленные сильные стороны
            - Предупреждение о возможных рисках (эмоциональных, когнитивных)
            """
        else:
            prompt = """
            Analyze this child's drawing and provide a brief interpretation (no more than one paragraph) for each of the following points:
            1. Psychological age of the child
            2. Level of imagination and intelligence development
            3. Emotional intelligence
            4. Level of mental and emotional development
            5. Physical and psychological state
            
            Also provide specific recommendations for parents:
            - How to talk to the child about possible issues
            - How to develop the identified strengths
            - Warning about possible risks (emotional, cognitive)
            """
        
        # Отправляем запрос к OpenAI с изображением
        with open(file_path, "rb") as image_file:
            response = await client.chat.completions.create(
                model="gpt-4-vision-preview",  # Используем модель с поддержкой анализа изображений
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/{file_extension[1:]};base64,{base64.b64encode(image_file.read()).decode('utf-8')}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1000
            )
        
        # Парсим ответ от OpenAI
        analysis_text = response.choices[0].message.content
        
        # Простой парсинг результатов (в реальном приложении нужен более надежный парсер)
        sections = analysis_text.split("\n\n")
        results = {}
        
        for section in sections:
            if "психологический возраст" in section.lower() or "psychological age" in section.lower():
                results["psychologicalAge"] = section
            elif "воображения и интеллекта" in section.lower() or "imagination and intelligence" in section.lower():
                results["imaginationLevel"] = section
            elif "эмоциональный интеллект" in section.lower() or "emotional intelligence" in section.lower():
                results["emotionalIntelligence"] = section
            elif "умственного и эмоционального развития" in section.lower() or "mental and emotional development" in section.lower():
                results["developmentLevel"] = section
            elif "физическое и психологическое" in section.lower() or "physical and psychological" in section.lower():
                results["physicalState"] = section
            elif "рекомендации" in section.lower() or "recommendations" in section.lower():
                results["recommendations"] = section
        
        # Возвращаем результаты анализа
        return results
        
    except Exception as e:
        # Логирование ошибки
        print(f"Error analyzing image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ошибка при анализе изображения: {str(e)}")
    finally:
        # Удаляем временный файл
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)

if __name__ == "__main__":
    import uvicorn
    # Получаем порт из переменной окружения или используем 8080 по умолчанию
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)