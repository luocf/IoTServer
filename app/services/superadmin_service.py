import os
import hashlib
from sqlalchemy.orm import Session
from app import crud
from app.utils import send_sms_verification, verify_sms_code
from app.schemas import SystemCreate, SystemUpdate

def handle_background_image_upload(db: Session, systemID: str, file_content: bytes, file_name: str):
    # 打印函数的输入参数
    print(f"Uploading image for systemID: {systemID}, file_name: {file_name}")
    
    # 假设生成了一个file_token
    file_token = "generated_token"
    
    print(f"Generated file_token: {file_token}")
    
    return file_token, None

def verify_superadmin_credentials(db: Session, superID: str, superPasswd: str):
    return crud.get_admin_by_credentials(db, superID, superPasswd)

def handle_sms_verification(superID: str):
    print(f"Sending SMS verification code to {superID}")
    return send_sms_verification(superID) != -1

def handle_superadmin_login(superID: str, verifyCode: str):
    return verify_sms_code(superID, verifyCode)

def get_system_by_name(db: Session, newSystem: str):
    return crud.get_system_by_name(db, newSystem)


def create_new_system_service(db: Session, system_data: SystemCreate):
    try:
        return crud.create_new_system(db, system_data)
    except Exception as e:
        # 日志记录异常信息
        print(f"Error creating system: {e}")
        return None
    
def modify_existing_system(db: Session, system_data: SystemUpdate):
    return crud.update_system(db, system_data)

def change_system_status_service(db: Session, systemID: str, status: bool):
    return crud.change_system_status(db, systemID, status)


def validate_superadmin(db: Session, super_id: str) -> bool:
    superadmin = crud.get_superadmin_by_id(db, super_id)
    return superadmin is not None

def list_managed_systems_service(db: Session, first: int = 0, number: int = 0):
    return crud.list_systems(db, first, number)
