from app.db.session import engine
from app.models.base import Base
# 모델들을 임포트해야 Base.metadata가 이를 인식합니다.
from app.models.item import Item
from app.models.file_model import UploadedFile

async def init_tables():
    async with engine.begin() as conn:
        # DB에 테이블 생성 (이미 존재하면 건너뜀)
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database tables created successfully.")
