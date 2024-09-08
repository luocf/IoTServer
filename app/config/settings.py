import secrets

#用于加密和解密数据的密钥。它用于生成和验证 JWT（JSON Web Tokens）、加密会话数据等。
SECRET_KEY = secrets.token_hex(32)  # 生成一个 64 字符的十六进制字符串

#用于加密和解密 JWT 的算法。例如，常用的算法有 HS256（HMAC 使用 SHA-256）、RS256（RSA 使用 SHA-256）等。
ALGORITHM = "HS256"  # 选择对称加密算法

#设置访问令牌（Access Token）的过期时间，以分钟为单位。
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 访问令牌过期时间为 60 分钟