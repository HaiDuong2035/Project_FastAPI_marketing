import bcrypt
from jose import jwt
from datetime import datetime, timedelta, timezone
from core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS

def hash_password(password: str):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

def create_access_token(data: dict):
    return jwt.encode(
        {
            **data,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        },
        SECRET_KEY,
        ALGORITHM
    )

def create_refresh_token(data: dict):
    return jwt.encode(
        {
            **data,
            "exp": datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        },
        SECRET_KEY,
        ALGORITHM
    )

def decode_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, ALGORITHM)
    except:
        return None