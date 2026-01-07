from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.init_db import init_table
from app.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 앱 시작시 실행
    await init_table()
    yield
    # 앱 종료시 실행(필요시)


app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message": "Hello World from FastAPI & Docker", "db_url": "Loaded successfully"}

@app.get("/health")
def health_check():
    return {"status": "ok"}