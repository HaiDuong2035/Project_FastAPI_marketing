from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timezone

from models.user import UserModel
from models.campaign_member import CampaignMemberModel
from models.campaign_task import CampaignTaskModel
from models.campaign_task_comment import CampaignTaskCommentModel
from schemas.campaign_task_comment import CampaignTaskCommentCreate

def create_task_comment(task_id: int, in_comment: CampaignTaskCommentCreate, current_user: UserModel, db: Session):
    task = db.query(CampaignTaskModel).filter(CampaignTaskModel.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy đầu việc"
        )
    member_db = (
        db.query(CampaignMemberModel)
        .filter(
            CampaignMemberModel.campaign_id == task.campaign_id,
            CampaignMemberModel.user_id == current_user.id
        )
        .first()
    )
    if not member_db:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không thuộc chiến dịch này"
        )
    new_comment = CampaignTaskCommentModel(
        campaign_task_id=task.id,
        user_id=current_user.id,
        content=in_comment.content,
        created_at=datetime.now(timezone.utc)
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

def get_task_comments(task_id: int, current_user: UserModel, db: Session):
    task = db.query(CampaignTaskModel).filter(CampaignTaskModel.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy đầu việc"
        )
    member_db = (
        db.query(CampaignMemberModel)
        .filter(
            CampaignMemberModel.campaign_id == task.campaign_id,
            CampaignMemberModel.user_id == current_user.id
        )
        .first()
    )
    if not member_db:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền xem comment"
        )
    return (
        db.query(CampaignTaskCommentModel)
        .filter(CampaignTaskCommentModel.campaign_task_id == task_id)
        .order_by(CampaignTaskCommentModel.created_at.asc())
        .all()
    )