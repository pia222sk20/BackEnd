from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

@app.get("/")
def read_root():
    return {"message": "Hello World from FastAPI & Docker", "db_url": "Loaded successfully"}

@app.get("/health")
def health_check():
    return {"status": "ok"}