from datetime import datetime, timedelta
import requests
import time
import jwt
from dotenv import load_dotenv
import os

load_dotenv()  # 加载 .env 文件中的环境变量
SECRET_KEY = os.getenv("SECRET_KEY")# 用于签名 token 的密钥

def generate_admin_token(admin_id: str) -> str:
    payload = {
        "admin_id": admin_id,
        "exp": datetime.utcnow() + timedelta(hours=1)  # 1 小时后过期
    }
    # 假设你使用 JWT 或其他方式生成 token
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

# 假设我们用一个字典存储验证码和过期时间（TODO 为了示例）
verification_store = {}

def format_date(date_str: str) -> datetime:
    return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")

# 其他工具函数

# utils.py
def send_sms_verification(superID: str) -> int:
    # 假设我们生成一个验证码
    verification_code = generate_verification_code()
    
    # 配置短信服务的 API URL 和请求参数 TODO
    sms_service_url = "https://api.smsprovider.com/send"
    payload = {
        "to": superID,  # 这里假设 superID 是手机号码
        "message": f"您的验证码是 {verification_code}"
    }
    
    # 发送请求到短信服务 TODO
    try:
        # response = requests.post(sms_service_url, json=payload)
        # response.raise_for_status()  # 如果响应状态码不是 200，将引发 HTTPError
        # 如果发送成功，将验证码存储在 verification_store 中
        store_verification_code(superID, verification_code)
        
        return verification_code
    except requests.RequestException as e:
        print(f"发送短信验证码失败: {e}")
        return -1

def generate_verification_code() -> str:
    # 生成一个随机的验证码
    import random
    # return str(random.randint(100000, 999999))
    return "valid_verifyCode" # TODO 为了测试方便，我们固定验证码为 "valid_verifyCode"

    
def remove_verification_code(superID: str) -> None:
    if superID in verification_store:
        del verification_store[superID]
        
def store_verification_code(superID: str, code: str) -> None:
    expiration_time = time.time() + 300  # 5分钟有效期
    verification_store[superID] = {"code": code, "expires_at": expiration_time}

def verify_sms_code(superID: str, code: str) -> bool:
    # 从存储中获取验证码信息
    stored_info = verification_store.get(superID)
    
    if not stored_info:
        return False
    
    # 检查验证码是否过期
    if time.time() > stored_info["expires_at"]:
        # 过期后删除验证码
        remove_verification_code(superID)
        return False
    
    # 验证码是否匹配
    return stored_info["code"] == code
