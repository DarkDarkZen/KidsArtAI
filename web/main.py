from fastapi import FastAPI, Request, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import json

app = FastAPI()

# Подключение статических файлов для JavaScript
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
        "status": "DrawingMind is running", 
        "version": "1.0.0",
        "environment": os.environ.get("RAILWAY_ENVIRONMENT", "unknown")
    })

@app.post("/api/analyze")
async def analyze_drawing(image: UploadFile = File(...)):
    """
    API-эндпоинт для анализа детского рисунка.
    В демо-версии возвращает заранее подготовленные результаты.
    """
    try:
        # Проверка типа файла
        if not image.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # В демо-версии возвращаем заранее подготовленные результаты
        demo_results = {
            "psychologicalAge": "The drawing suggests a psychological age of around 5-6 years, which is characterized by the use of basic shapes and simplified representations of figures. The child is in the pre-schematic stage of artistic development.",
            "imaginationLevel": "The child demonstrates a moderate level of imagination, shown through the creative use of colors and the inclusion of various elements in the drawing. There's potential for further development with proper stimulation.",
            "emotionalIntelligence": "The drawing indicates a developing emotional intelligence. The child appears to understand basic emotions, as shown by the facial expressions in the drawing, but may need support in recognizing more complex emotional states.",
            "developmentLevel": "The mental and emotional development appears age-appropriate. The child shows the ability to organize thoughts and represent them visually, which is a positive sign of cognitive development.",
            "physicalState": "The drawing suggests normal physical development for the child's age. The pressure applied to the drawing tool and the control shown in creating lines indicate appropriate fine motor skills development.",
            "recommendations": "Encourage the child to explain their drawings to develop verbal expression. Provide various art materials to explore different textures and techniques. Consider regular drawing sessions where the child can express daily experiences, which will help develop emotional processing skills."
        }
        
        return demo_results
        
    except Exception as e:
        # Логирование ошибки
        print(f"Error analyzing image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error analyzing image: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    # Получаем порт из переменной окружения или используем 8080 по умолчанию
    port = int(os.environ.get("PORT", 8080))
    print(f"Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)