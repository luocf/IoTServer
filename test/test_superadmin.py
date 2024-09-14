from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app  # 假设你的 FastAPI 应用实例在 app/main.py 中
from app.db import SessionLocal

import os
from app.models import System

client = TestClient(app)
def test_get_sms_verification_success(test_superadmin):
    response = client.get("/api/superadmin/get_sms_verification", params={
        "superID": "test_superID",
        "superPasswd": "test_superPasswd",
        "needAnswer": "no"
    })
    assert response.status_code == 200
    assert response.json() == {"what": "GET_SUPERVERIFY", "code": "0"}


def test_get_sms_verification_failure():
    response = client.get("/api/superadmin/get_sms_verification", params={
        "superID": "invalid_superID",
        "superPasswd": "invalid_superPasswd",
        "needAnswer": "no"
    })
    assert response.status_code == 400
    assert response.json() == {"what": "GET_SUPERVERIFY", "code": "3", "errNo": "1", "errMsg": "获取验证码失败"}
    
def test_superadmin_login_success():
    response = client.post("/api/superadmin/login", json={
        "superID": "test_superID",
        "superPasswd": "test_superPasswd",
        "verifyCode": "valid_verifyCode",
        "needAnswer": "yes"
    })
    assert response.status_code == 200
    assert response.json() == {"what": "SET_SUPERLOGIN", "code": "OK"}

def test_superadmin_login_failure():
    response = client.post("/api/superadmin/login", json={
        "superID": "test_superID",
        "superPasswd": "test_superPasswd",
        "verifyCode": "invalid_verifyCode",
        "needAnswer": "yes"
    })
    assert response.status_code == 400
    assert response.json() == {
        "detail": {
            "what": "SET_SUPERLOGIN",
            "code": "3",
            "errNo": "3",
            "errMsg": "验证码错误"
        }
    }

def test_check_system_availability_success():
    response = client.post("/api/superadmin/check_system_availability", json={
        "newSystem": "newSystemName",
        "adminID": "adminID"
    })
    assert response.status_code == 200
    assert response.json() == {"what": "QRY_SUPERSYSTEM", "code": "0", "systemID": "available"}

def test_create_new_system_success(test_system):
    response = client.post("/api/superadmin/create_system", json={
        "systemID": "systemID",
        "newSystem": "newSystem3",
        "adminID": "adminID",
        "adminPasswd": "adminPasswd",
        "adminPhoneNum": "1234567890"
    })
    
    assert response.status_code == 200
    assert response.json() == {
        "what": "SET_SUPERNEW",
        "code": "0",
        "token": "adminToken"
    }
def test_modify_system_success():
    response = client.post("/api/superadmin/modify_system", json={
        "systemID": "systemID",#mock systemID
        "systemName": "modifiedSystemName",
        "adminID": "adminID",
        "passwd": "newAdminPasswd",
        "phoneNum": "0987654321"
    })
    assert response.status_code == 200

    
def get_all_systems():
    db = SessionLocal()
    systems = db.query(System).all()  # 获取所有记录
    
    for system in systems:
        print(f"System ID: {system.system_id}, System Name: {system.system_name}")

    db.close()  # 记得关闭数据库会话
def test_traverse_systems():
    db = SessionLocal()
    
    # 获取所有系统记录
    systems = db.query(System).all()
    
    # 遍历并打印所有系统记录
    for system in systems:
        print(f"System ID: {system.system_id}, System Name: {system.system_name}")
    
    assert len(systems) > 0, "No systems found in the database."
    
    db.close()  # 关闭会话
    
def test_upload_background_image_success():
     # 检查是否有 systemID 为 'systemID' 的记录
    db = SessionLocal()
    test_traverse_systems()
    
    system_exists = db.query(System).filter(System.system_id == "systemID").first()
    assert system_exists is not None, "System with systemID='systemID' does not exist in the database."
    
    file_path = os.path.join(os.path.dirname(__file__), "test_image.png")
    
    with open(file_path, "rb") as file:
        # 使用 multipart/form-data 传递文件
        response = client.post(
            "/api/superadmin/upload_background_image/?systemID=systemID",  # systemID 通过查询参数传递
            files={"pngFile": ("test_image.png", file, "image/png")}  # 正确传递文件名、文件内容和MIME类型
        )

    print(response.json())  # 打印响应以调试
    assert response.status_code == 200


def test_manage_system_success():
    response = client.post("/api/superadmin/manage_system", params={
        "systemID": "systemID",
        "manage": "enable"
    })
    assert response.status_code == 200
    assert response.json() == {"what": "SET_SUPERMANAGE", "code": "OK"}

def test_list_managed_systems_success():
    response = client.get("/api/superadmin/list_systems", params={
        "superID": "test_superID",
        "first": 0,
        "number": 10
    })
    assert response.status_code == 200
    assert "system" in response.json()
    assert response.json()["what"] == "GET_SUPERLIST"
    assert response.json()["code"] == "0"

# 运行测试
if __name__ == "__main__":
    import pytest
    pytest.main()
