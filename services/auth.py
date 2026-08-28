from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timezone

from schemas.auth import UserRegisterInput, UserLoginInput
from models.user import UserModel
from core.security import hash_password, check_password, create_access_token, create_refresh_token, decode_token

refresh_token_storage = {}

def register(in_user: UserRegisterInput, db: Session):
    if db.query(UserModel).filter(UserModel.email == in_user.email).first():
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "Email đã tồn tại"
        )
    new_user = UserModel(
        email = in_user.email,
        password_hash = hash_password(in_user.password),
        full_name = in_user.full_name,
        created_at = datetime.now(timezone.utc)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login(in_user: UserLoginInput, db: Session):
    user_db = db.query(UserModel).filter(UserModel.email == in_user.email).first()
    if not user_db:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "Đăng nhập thất bại"
        )
    if not check_password(in_user.password, user_db.password_hash):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "Đăng nhập thất bại"
        )
    access_token = create_access_token({
        "email": user_db.email,
        "role": user_db.role
    })
    refresh_token_storage["token"] = create_refresh_token({"email": user_db.email})
    return access_token

def refresh_access_token(db: Session):
    refresh_token = refresh_token_storage.get("token")
    if refresh_token:
        payload = decode_token(refresh_token)
        if payload:
            user_db = db.query(UserModel).filter(UserModel.email == payload["email"]).first()
            if not user_db:
                raise HTTPException(
                    status.HTTP_401_UNAUTHORIZED,
                    "Không tìm thấy người dùng"
                )
            return create_access_token({
                "email": user_db.email,
                "role": user_db.role
            })
    raise HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        "Refresh token hết hạn/không hợp lệ, vui lòng đăng nhập lại"
    )