from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from models.user import UserModel
from core.middleware import get_current_user
from db.database import get_db
from schemas.user import UserResponse
from services import user

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserResponse)
def get_my_infor(current_user: UserModel = Depends(get_current_user)):
    return current_user

@router.get("", response_model=List[UserResponse])
def search_users(
    keyword_name: str = None,
    keyword_email: str = None,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return user.search_users(current_user, db, keyword_name, keyword_email)