from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from services import auth
from schemas.auth import UserRegisterInput, UserLoginInput
from db.database import get_db
from core.middleware import login_rate_limit

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(in_user: UserRegisterInput, db: Session = Depends(get_db)):
    return auth.register(in_user, db)

@router.post("/login")
def login(in_uer: UserLoginInput, db: Session = Depends(get_db)):
    login_rate_limit()
    return {
        "message": "Đăng nhập thành công",
        "token": auth.login(in_uer, db)
    }

@router.post("/refresh-access-token")
def refresh_access_token(db: Session = Depends(get_db)):
    return {
        "access token": auth.refresh_access_token(db)
    }