from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import get_db
from schemas.campaign_task import TaskStatus, TaskPriority
from schemas.campaign_task_comment import CampaignTaskCommentCreate
from services import campaign_task, campaign_task_comment
from models.user import UserModel
from core.middleware import get_current_user

router = APIRouter(prefix="/campaign-tasks/{task_id}", tags=["Campaign Task"])

@router.get("")
def get_campaign_task_by_id(
    task_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return campaign_task.get_campaign_task_by_id(task_id, current_user, db)

@router.patch("")
def update_campaign_task(
    task_id: int,
    title: str = None,
    description: str = None,
    assignee_id: int = None,
    task_status: TaskStatus = None,
    priority: TaskPriority = None,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return campaign_task.update_campaign_task(
        task_id=task_id,
        current_user=current_user,
        db=db,
        title=title,
        description=description,
        assignee_id=assignee_id,
        task_status=task_status,
        priority=priority
    )

@router.delete("")
def delete_campaign_task(
    task_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return campaign_task.delete_campaign_task(task_id, current_user, db)

@router.post("/comments")
def create_task_comment(
    task_id: int,
    in_comment: CampaignTaskCommentCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return campaign_task_comment.create_task_comment(task_id, in_comment, current_user, db)

@router.get("/comments")
def get_task_comments(
    task_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return campaign_task_comment.get_task_comments(task_id, current_user, db)