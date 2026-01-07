from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.config import settings
from app.db.init_db import init_tables
from app.api.v1.api import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 앱 시작 시 실행
    await init_tables()
    yield
    # 앱 종료 시 실행 (필요하다면)

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

# API 라우터 등록
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def read_root():
    return {"message": "Hello World from FastAPI & Docker", "config_check": settings.PROJECT_NAME}

@app.get("/health")
def health_check():
    return {"status": "ok"}