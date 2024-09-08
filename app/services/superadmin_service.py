import os
import hashlib
from sqlalchemy.orm import Session
from app.crud import (
    get_admin_by_credentials,
    get_system_by_name,
    create_new_system,
    update_system,
    change_system_status,
    list_systems,
    get_system_by_id, 
    save_background_image,
    get_superadmin_by_id
)
from app.utils import send_sms_verification, verify_sms_code
from app.schemas import SystemCreate, SystemUpdate

def handle_background_image_upload(db: Session, system_id: str, png_file: bytes, file_name: str) -> str:
    # 检查系统是否存在
    system = get_system_by_id(db, system_id)
    if not system:
        return None, "系统不存在"

    # 生成文件的 token 名称以避免重复
    file_hash = hashlib.md5(png_file).hexdigest()
    file_token = f"{file_hash}.png"
    
    # 保存文件到指定目录
    file_path = f"/usr/local/nginx/html/bkimage/{file_token}"
    try:
        with open(file_path, "wb") as f:
            f.write(png_file)
        save_background_image(db, system_id, file_token, file_path, file_name)  # 保存背景图信息到数据库
    except Exception as e:
        return None, "上传文件失败"

    return file_token, None

def verify_superadmin_credentials(db: Session, superID: str, superPasswd: str):
    return get_admin_by_credentials(db, superID, superPasswd)

def handle_sms_verification(superID: str):
    return send_sms_verification(superID) != -1

def handle_superadmin_login(superID: str, verifyCode: str):
    return verify_sms_code(superID, verifyCode)

def get_system_by_name(db: Session, newSystem: str):
    return get_system_by_name(db, newSystem)


def create_new_system_service(db: Session, system_data: SystemCreate):
    try:
        return create_new_system(db, system_data)
    except Exception as e:
        # 日志记录异常信息
        print(f"Error creating system: {e}")
        return None
    
def modify_existing_system(db: Session, systemID: str, system_data: SystemUpdate):
    return update_system(db, systemID, system_data)

def change_system_status_service(db: Session, systemID: str, status: bool):
    return change_system_status(db, systemID, status)


def validate_superadmin(db: Session, super_id: str) -> bool:
    superadmin = get_superadmin_by_id(db, super_id)
    return superadmin is not None

def list_managed_systems_service(db: Session, first: int = 0, number: int = 0):
    return list_systems(db, first, number)
