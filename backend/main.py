from fastapi import FastAPI
from routers.upload import router as upload_router

app = FastAPI(
    title="AI Refactoring Recommendation System",
    version="1.0"
)

app.include_router(upload_router)

@app.get("/")
def home():
    return {
        "status": "success",
        "message": "AI Refactoring Recommendation System is running!"
    }