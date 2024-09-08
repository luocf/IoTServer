from typing import Optional
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models import User
from app.config import settings
from app.crud import (
    create_user,
    get_user_by_id
)

from app.utils import send_sms_verification, verify_sms_code
# 密码加密配置
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT 配置
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

class UserService:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def register_user(db: Session, user_id: str, user_name: str, phone_num: str, password: str, verify_code: str) -> str:
        hashed_password = UserService.get_password_hash(password)
        
        # 将数据库操作委托给 CRUD 层
        new_user = create_user(db, user_id, phone_num, hashed_password)
        
        token_data = {"sub": new_user.user_id}
        return UserService.create_access_token(data=token_data)
 
    @staticmethod
    def get_user_by_id(db: Session, user_id: str) -> User:
        return get_user_by_id(db, user_id)
    
    @staticmethod
    def verify_code(user: User, code: str) -> bool:
        # 假设验证码保存在用户的 profile 或者临时存储中
        return verify_sms_code(user.phone_number, code)
    
    @staticmethod
    def login_user(user, password: str) -> str:
        if not user or not UserService.verify_password(password, user.password):
            raise Exception("无效的用户ID或密码")
        token_data = {"sub": user.user_id}
        return UserService.create_access_token(data=token_data)
    
    @staticmethod
    def token_login_user(token: str) -> str:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: str = payload.get("sub")
            if user_id is None:
                raise Exception("无效的Token")
            return token  # Token 验证通过，返回原始Token
        except JWTError:
            raise Exception("无效的Token")
        
    
    @staticmethod
    def send_verification_code(db: Session, user_id: str, user_name: str, phone_number: str, password: str):
        # 检查用户是否已存在
        user = get_user_by_id(db, user_id)
        if user:
            raise Exception("用户已存在")

        send_sms_verification(phone_number)
        
    @staticmethod
    def get_login_verification_code(db: Session, user_id: str, password: str):
        user = get_user_by_id(db, user_id)
        if not user or not UserService.verify_password(password, user.password):
            raise Exception("无效的用户ID或密码")
        
        # 生成验证码&发送短信验证码
        verification_code = send_sms_verification(user.phone_number)

        # 你可以在这里选择将验证码存储在数据库中以供后续验证使用
        return verification_code