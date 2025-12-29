from fastapi import FastAPI,Depends,HTTPException,status
from fastapi.middleware.cors import CORSMiddleware   #  Django(8000) 와 FastAPI(8001) 연동시 필요  CORS 문제 해결
from sqlalchemy.orm import Session 
from typing import List
import models
import schemas
from database import engine, get_db

# 테이블 생성
models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Product API",
    description='제품관리',
    version='1.0.0'
)

# CROS 설정 - Django 와 FastAPI 연동시 필요
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000","http://127.0.0.1:8000"],
)


# 라우터 설정
@app.get('/')
def root():
    return {"message": "Welcome to the Product API"}

