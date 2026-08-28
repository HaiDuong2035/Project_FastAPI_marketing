from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.user import UserModel

def search_users(current_user: UserModel, db: Session, keyword_name: str = None, keyword_email: str = None):
    if current_user.role != "ADMIN":
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "Không đủ quyền để dùng chức năng"
        )
    result = db.query(UserModel)
    if keyword_name:
        result = result.filter(UserModel.full_name.like(f"%{keyword_name}%"))
    if keyword_email:
        result = result.filter(UserModel.full_name.like(f"%{keyword_email}%"))
    return result.all()