from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import get_db
from schemas.campaign_task import CampaignTaskUpdate
from schemas.campaign_task_comment import CampaignTaskCommentCreate
from services import campaign_task, campaign_task_comment
from models.user import UserModel
from core.middleware import get_current_user

router = APIRouter(prefix="/campaign-tasks", tags=["Campaign Task"])

@router.get("/{id}")
def get_campaign_task_by_id(
    id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return campaign_task.get_campaign_task_by_id(id, current_user, db)

@router.patch("/{id}")
def update_campaign_task(
    id: int,
    in_task: CampaignTaskUpdate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return campaign_task.update_campaign_task(id, in_task, current_user, db)

@router.delete("/{id}")
def delete_campaign_task(
    id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return campaign_task.delete_campaign_task(id, current_user, db)

@router.post("/{id}/comments")
def create_task_comment(
    id: int,
    in_comment: CampaignTaskCommentCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return campaign_task_comment.create_task_comment(id, in_comment, current_user, db)

@router.get("/{id}/comments")
def get_task_comments(
    id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return campaign_task_comment.get_task_comments(id, current_user, db)