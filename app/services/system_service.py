from sqlalchemy.orm import Session
from app.crud import (
    get_admin_by_credentials,
    get_system_by_name,
    create_new_system,
    update_system,
    change_system_status,
    list_systems
)
from app.utils import send_sms_verification, verify_sms_code
from app.schemas import SystemCreate, SystemUpdate

def verify_superadmin_credentials(db: Session, superID: str, superPasswd: str):
    return get_admin_by_credentials(db, superID, superPasswd)

def handle_sms_verification(superID: str):
    return send_sms_verification(superID) != -1

def handle_superadmin_login(superID: str, verifyCode: str):
    return verify_sms_code(superID, verifyCode)

def check_system_availability(db: Session, newSystem: str):
    return get_system_by_name(db, newSystem) is None

def create_new_system_service(db: Session, system_data: SystemCreate):
    return create_new_system(db, system_data)

def modify_existing_system(db: Session, systemID: str, system_data: SystemUpdate):
    return update_system(db, systemID, system_data)

def change_system_status_service(db: Session, systemID: str, status: bool):
    return change_system_status(db, systemID, status)

def list_managed_systems_service(db: Session, first: int = 0, number: int = 10):
    return list_systems(db, first, number)
