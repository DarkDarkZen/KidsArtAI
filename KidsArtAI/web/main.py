from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/health")
async def health_check():
    return JSONResponse({"status": "healthy"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 