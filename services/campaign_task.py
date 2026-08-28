from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timezone

from models.user import UserModel
from models.campaign import CampaignModel
from models.campaign_member import CampaignMemberModel
from models.campaign_task import CampaignTaskModel
from schemas.campaign_task import CampaignTaskCreate, TaskPriority, TaskStatus, SortType

def create_campaign_task(
    campaign_id: int,
    in_task: CampaignTaskCreate,
    current_user: UserModel,
    db: Session
):
    campaign_db = (
        db.query(CampaignModel)
        .filter(
            CampaignModel.id == campaign_id,
            CampaignModel.is_delete.is_(False)
        )
        .first()
    )
    if not campaign_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy chiến dịch"
        )
    member_db = (
        db.query(CampaignMemberModel)
        .filter(
            CampaignMemberModel.campaign_id == campaign_id,
            CampaignMemberModel.user_id == current_user.id
        )
        .first()
    )
    if not member_db:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không thuộc chiến dịch này"
        )
    if in_task.assignee_id is not None:
        if  member_db.role != "OWNER":
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                "Chỉ owner mới có thể giao task, để trống assignee_id nếu bạn không phải owner"
            )
        assignee = (
            db.query(UserModel)
            .filter(UserModel.id == in_task.assignee_id)
            .first()
        )
        if not assignee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Không tồn tại người được giao việc"
            )
        assignee_member = (
            db.query(CampaignMemberModel)
            .filter(
                CampaignMemberModel.campaign_id == campaign_id,
                CampaignMemberModel.user_id == in_task.assignee_id
            )
            .first()
        )
        if not assignee_member:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Không thể gán task cho user ngoài chiến dịch"
            )
    new_task = CampaignTaskModel(
        campaign_id=campaign_id,
        title=in_task.title,
        assignee_id=in_task.assignee_id,
        status="TODO",
        description=in_task.description,
        priority=in_task.priority,
        due_date=in_task.due_date,
        created_at=datetime.now(timezone.utc),
        created_by_id=current_user.id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def get_campaign_tasks(
    campaign_id: int,
    current_user: UserModel,
    db: Session,
    task_status: TaskStatus = None,
    priority: TaskPriority = None,
    assignee_id: int = None,
    keyword: str = None,
    limit: int = 10,
    offset: int = 0,
    sort_by: SortType = "CREATED_AT"
):
    member_db = (
        db.query(CampaignMemberModel)
        .filter(
            CampaignMemberModel.campaign_id == campaign_id,
            CampaignMemberModel.user_id == current_user.id
        )
        .first()
    )
    if not member_db:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không thuộc chiến dịch này"
        )
    query = db.query(CampaignTaskModel).filter(CampaignTaskModel.campaign_id == campaign_id)
    if task_status:
        query = query.filter(CampaignTaskModel.status == task_status)
    if priority:
        query = query.filter(CampaignTaskModel.priority == priority)
    if assignee_id is not None:
        query = query.filter(CampaignTaskModel.assignee_id == assignee_id)
    if keyword:
        query = query.filter(CampaignTaskModel.title.like(f"%{keyword}%"))
    if sort_by == "DUE_DATE":
        query = query.order_by(CampaignTaskModel.due_date)
    else:
        query = query.order_by(CampaignTaskModel.created_at.desc())
    return query.offset(offset).limit(limit).all()

def get_campaign_task_by_id(
    task_id: int,
    current_user: UserModel,
    db: Session
):
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
    return task

def update_campaign_task(
    task_id: int,
    current_user: UserModel,
    db: Session,
    title: str = None,
    description: str = None,
    assignee_id: int = None,
    task_status: TaskStatus = None,
    priority: TaskPriority = None
):
    task = (
        db.query(CampaignTaskModel)
        .filter(CampaignTaskModel.id == task_id)
        .first()
    )
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy đầu việc"
        )
    campaign = (
        db.query(CampaignModel)
        .filter(
            CampaignModel.id == task.campaign_id,
            CampaignModel.is_delete.is_(False)
        )
        .first()
    )
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy chiến dịch"
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
    is_owner = campaign.owner_id == current_user.id
    is_creator = task.created_by_id == current_user.id
    is_assignee = task.assignee_id == current_user.id
    if not (is_owner or is_creator or is_assignee):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền cập nhật đầu việc"
        )
    update_data = {}
    if title is not None:
        update_data["title"] = title
    if description is not None:
        update_data["description"] = description
    if assignee_id is not None:
        update_data["assignee_id"] = assignee_id
    if task_status is not None:
        update_data["status"] = task_status
    if priority is not None:
        update_data["priority"] = priority
    if is_assignee and not is_owner and not is_creator:
        invalid_fields = set(update_data.keys()) - {"status"}
        if invalid_fields:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Assignee chỉ được cập nhật trạng thái"
            )
    if "assignee_id" in update_data:
        new_assignee = (
            db.query(CampaignMemberModel)
            .filter(
                CampaignMemberModel.campaign_id == task.campaign_id,
                CampaignMemberModel.user_id == update_data["assignee_id"]
            )
            .first()
        )
        if not new_assignee:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Assignee không thuộc chiến dịch"
            )
    for key, value in update_data.items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task

def delete_campaign_task(task_id: int, current_user: UserModel, db: Session):
    task = db.query(CampaignTaskModel).filter(CampaignTaskModel.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy đầu việc"
        )
    campaign = (
        db.query(CampaignModel)
        .filter(
            CampaignModel.id == task.campaign_id,
            CampaignModel.is_delete.is_(False)
        )
        .first()
    )
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy chiến dịch"
        )
    is_owner = campaign.owner_id == current_user.id
    is_creator = task.created_by_id == current_user.id
    if not is_owner and not is_creator:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền xóa đầu việc"
        )
    db.delete(task)
    db.commit()
    return