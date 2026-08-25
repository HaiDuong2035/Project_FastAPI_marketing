from sqlalchemy.orm import Session, joinedload
from datetime import datetime, timezone
from fastapi import HTTPException, status

from schemas.campaign import CampaignCreate, CampaignUpdate
from models.user import UserModel
from models.campaign import CampaignModel
from models.campaign_member import CampaignMemberModel
from models.campaign_log import CampaignLogModel

def create_campaign(
    in_campaign: CampaignCreate,
    current_user: UserModel,
    db: Session
):
    new_campaign = CampaignModel(
        name=in_campaign.name,
        description=in_campaign.description,
        owner_id=current_user.id,
        created_at=datetime.now(timezone.utc)
    )
    db.add(new_campaign)
    db.flush()
    new_campaign_member = CampaignMemberModel(
        campaign_id=new_campaign.id,
        user_id=current_user.id,
        role="OWNER",
        joined_at=datetime.now(timezone.utc)
    )
    new_campaign_log = CampaignLogModel(
        campaign_id=new_campaign.id,
        user_id=current_user.id,
        activity="CREATE",
        did_at=datetime.now(timezone.utc)
    )
    db.add_all([new_campaign_member, new_campaign_log])
    db.commit()
    return (
        db.query(CampaignModel)
        .options(joinedload(CampaignModel.owner))
        .filter(CampaignModel.id == new_campaign.id)
        .first()
    )

def search_campaigns(
    keyword: str | None,
    current_user: UserModel,
    db: Session
):
    query = (
        db.query(CampaignModel)
        .join(
            CampaignMemberModel,
            CampaignMemberModel.campaign_id == CampaignModel.id
        )
        .options(
            joinedload(CampaignModel.owner),
            joinedload(CampaignModel.campaign_members)
            .joinedload(CampaignMemberModel.user)
        )
        .filter(
            CampaignMemberModel.user_id == current_user.id,
            CampaignModel.is_delete.is_(False)
        )
    )
    if keyword:
        query = query.filter(
            CampaignModel.name.like(f"%{keyword}%")
        )
    return query.all()

def find_campaign_by_id(id: int, current_user: UserModel, db: Session):
    campaign_db = (
        db.query(CampaignModel)
        .join(
            CampaignMemberModel,
            CampaignMemberModel.campaign_id == CampaignModel.id
        )
        .filter(
            CampaignModel.id == id,
            CampaignMemberModel.user_id == current_user.id,
            CampaignModel.is_delete.is_(False)
        )
        .first()
    )
    if not campaign_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy chiến dịch hoặc bạn không tham gia chiến dịch"
        )
    return (
        db.query(CampaignModel)
        .options(
            joinedload(CampaignModel.owner)
        )
        .filter(CampaignModel.id == id)
        .first()
    )

def update_campaign(id: int, in_campaign: CampaignUpdate, current_user: UserModel, db: Session):
    campaign_db = (
        db.query(CampaignModel)
        .filter(
            CampaignModel.id == id,
            CampaignModel.is_delete.is_(False)
        )
        .first()
    )
    if not campaign_db:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "Không tìm thấy chiến dịch"
        )
    if campaign_db.owner_id != current_user.id:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "Bạn không có quyền chỉnh sửa chiến dịch"
        )
    for key, value in in_campaign.model_dump(exclude_unset=True).items():
        setattr(campaign_db, key, value)
    new_campaign_log = CampaignLogModel(
        campaign_id = campaign_db.id,
        user_id = campaign_db.owner_id,
        activity = "UPDATE",
        did_at = datetime.now(timezone.utc)
    )
    db.add(new_campaign_log)
    db.commit()
    db.refresh(campaign_db)
    db.refresh(new_campaign_log)
    return (
        db.query(CampaignModel)
        .options(
            joinedload(CampaignModel.owner)
        )
        .filter(CampaignModel.id == campaign_db.id)
        .first()
    )

def delete_campaign(id: int, current_user: UserModel, db: Session):
    campaign_db = (
        db.query(CampaignModel)
        .filter(
            CampaignModel.id == id,
            CampaignModel.is_delete.is_(False)
        )
        .first()
    )
    if not campaign_db:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "Không tìm thấy chiến dịch"
        )
    if campaign_db.owner_id != current_user.id:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "Bạn không có quyền xóa chiến dịch"
        )
    campaign_db.is_delete = True
    new_campaign_log = CampaignLogModel(
        campaign_id = campaign_db.id,
        user_id = campaign_db.owner_id,
        activity = "DELETE",
        did_at = datetime.now(timezone.utc)
    )
    db.add(new_campaign_log)
    db.commit()
    db.refresh(campaign_db)
    db.refresh(new_campaign_log)
    return