from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import DeclarativeBase

# SQLAlchemy 2.0 스타일
class Base(DeclarativeBase):
    pass

# (선택) 공통 기능을 가진 Mixin 등을 여기에 정의할 수 있습니다.
# 예: 생성시간, 수정시간 자동 업데이트 등
