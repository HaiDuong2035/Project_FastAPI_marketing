from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from db.database import get_db
from schemas.campaign import CampaignCreate, CampaignUpdate, CampaignResponse
from schemas.campaign_member import CampaignMemberResponse
from schemas.campaign_task import CampaignTaskCreate, TaskPriority, TaskStatus
from services import campaign, campaign_member, campaign_task
from models.user import UserModel
from core.middleware import get_current_user

router = APIRouter(prefix="/campaigns", tags=["Campaign"])

@router.post("", status_code=status.HTTP_201_CREATED, response_model=CampaignResponse)
def create_campaign(
    in_campaign: CampaignCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return campaign.create_campaign(in_campaign, current_user, db)

@router.get("", response_model=List[CampaignResponse])
def search_campaigns(
    keyword: str = None,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    result = campaign.search_campaigns(keyword, current_user, db)
    if not result:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "Không tìm thấy chiến dịch/Bạn hiện không trong chiến dịch nào"
        )
    return result

@router.get("/{campaign_id}", response_model=CampaignResponse)
def find_campaign_by_id(
    campaign_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return campaign.find_campaign_by_id(campaign_id, current_user, db)

@router.put("/{campaign_id}", response_model=CampaignResponse)
def update_campaign(
    campaign_id: int,
    in_campaign: CampaignUpdate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return campaign.update_campaign(campaign_id, in_campaign, current_user, db)

@router.delete("/{campaign_id}")
def delete_campaign(
    campaign_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    campaign.delete_campaign(campaign_id, current_user, db)
    return {
        "message": "Xóa chiến dịch thành công"
    }

@router.post("/{campaign_id}/members")
def add_member(
    campaign_id: int,
    user_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return campaign_member.add_member(campaign_id, user_id, current_user, db)

@router.delete("/{campaign_id}/members/{user_id}")
def remove_member(
    campaign_id: int,
    user_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    campaign_member.delete_member(campaign_id, user_id, current_user, db)
    return {
        "message": "Đã loại bỏ thành viên khỏi chiến dịch"
    }

@router.get("/{campaign_id}/members", response_model=List[CampaignMemberResponse])
def get_members(
    campaign_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return campaign_member.get_members(campaign_id, current_user, db)

@router.post("/{campaign_id}/campaign-tasks")
def create_campaign_task(
    campaign_id: int,
    in_task: CampaignTaskCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return campaign_task.create_campaign_task(campaign_id, in_task, current_user, db)

@router.get("/{campaign_id}/campaign-tasks")
def get_campaign_tasks(
    campaign_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
    task_status: TaskStatus = None,
    priority: TaskPriority = None,
    assignee_id: int = None,
    keyword: str = None,
    limit: int = 10,
    offset: int = 0,
    sort_by: str = "created_at"
):
    return campaign_task.get_campaign_tasks(
        campaign_id,
        current_user,
        db, task_status,
        priority,
        assignee_id,
        keyword,
        limit,
        offset,
        sort_by
    )