# test/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db import Base, get_db, init_db
from app.models import SuperAdmin,System
from sqlalchemy.orm import Session

# 使用 SQLite 内存数据库进行测试
SQLALCHEMY_DATABASE_URL = "sqlite:///smart_park_management.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def db():
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    yield SessionLocal()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def test_superadmin(db: Session):
    # 清理之前的测试数据
    db.query(SuperAdmin).filter(SuperAdmin.super_admin_id == "test_superID").delete()
    db.query(System).filter(System.system_name == "newSystem3").delete()  # 清理冲突的 system_name

    db.commit()
    
    # 在测试数据库中添加 SuperAdmin 数据
    superadmin = SuperAdmin(
        super_admin_id="test_superID",  # 使用数据库表中定义的字段名称
        password="test_superPasswd",    # 使用数据库表中定义的字段名称
        phone_number="1234567890"       # 确保提供这个字段的值
    )
    db.add(superadmin)
    db.commit()
    return superadmin


@pytest.fixture(scope="function")
def test_system(db: Session):
    # 清理之前的测试数据
    db.query(System).filter(System.system_id == "systemID").delete()
    db.commit()