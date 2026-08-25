from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone

from core.security import decode_token
from db.database import get_db
from models.user import UserModel

security = HTTPBearer()

last_login_time = {}

def login_rate_limit():
    current_time = datetime.now(timezone.utc)
    last_time = last_login_time.get("last_time")
    if last_time:
        elapsed_time = current_time - last_time
        if elapsed_time < timedelta(seconds=30):
            raise HTTPException(
                status_code=429,
                detail="Đăng nhập bị giới hạn 30 giây kể từ lần đăng nhập gần nhất"
            )
    last_login_time["last_time"] = current_time

def get_current_user(cred: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = cred.credentials
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Token không hợp lệ/đã hết hạn"
        )

    user_db = db.query(UserModel).filter(UserModel.email == payload["email"]).first()
    if not user_db:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Không tìm thấy người dùng"
        )
    return user_db