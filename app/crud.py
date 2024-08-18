from sqlalchemy.orm import Session
from app.models import User, Space, Device
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_user(db: Session, user):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        return None

    hashed_password = get_password_hash(user.password)
    new_user = User(
        username=user.username,
        password=hashed_password,
        email=user.email,
        phone_number=user.phone_number,
        is_admin=user.is_admin,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def create_space(db: Session, space):
    db_space = Space(name=space.name, description=space.description)
    db.add(db_space)
    db.commit()
    db.refresh(db_space)
    return db_space

def get_space_by_id(db: Session, space_id: int):
    return db.query(Space).filter(Space.id == space_id).first()

def create_device(db: Session, device):
    db_device = Device(
        name=device.name,
        eui=device.eui,
        device_type=device.device_type,
        timeout=device.timeout,
        space_id=device.space_id,
        online_status=device.online_status,
        power_status=device.power_status,
        set_temperature=device.set_temperature,
        fan_speed=device.fan_speed,
        mode=device.mode
    )
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

def get_device_by_id(db: Session, device_id: int):
    return db.query(Device).filter(Device.id == device_id).first()
