from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Generator
from fastapi import Depends

# 数据库 URL（根据实际数据库配置进行调整）
DATABASE_URL = "sqlite:///smart_park_management.db"

# 创建数据库引擎
engine = create_engine(DATABASE_URL)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基本类，用于定义数据模型
Base = declarative_base()

# 初始化数据库，创建所有表
def init_db():
    from .models import Base  # Importing models here to avoid circular imports
    Base.metadata.create_all(bind=engine)

# 依赖项，用于获取数据库会话
def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
