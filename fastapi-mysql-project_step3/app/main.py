from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.config import settings
from app.db.init_db import init_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 앱 시작 시 실행
    await init_tables()
    yield
    # 앱 종료 시 실행 (필요하다면)

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message": "Hello World from FastAPI & Docker", "db_url": "Loaded successfully"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
