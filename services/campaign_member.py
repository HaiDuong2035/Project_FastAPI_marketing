from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from datetime import datetime, timezone

from models.user import UserModel
from models.campaign import CampaignModel
from models.campaign_member import CampaignMemberModel
from models.campaign_log import CampaignLogModel

def add_member(campaign_id: int, user_id: int, current_user: UserModel, db: Session):
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
    if campaign_db.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền thêm thành viên"
        )
    user_db = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy người dùng"
        )
    member_exists = (
        db.query(CampaignMemberModel)
        .filter(
            CampaignMemberModel.campaign_id == campaign_id,
            CampaignMemberModel.user_id == user_id
        )
        .first()
    )
    if member_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Người dùng đã tham gia chiến dịch"
        )
    new_member = CampaignMemberModel(
        campaign_id=campaign_id,
        user_id=user_id,
        role="MEMBER",
        joined_at=datetime.now(timezone.utc)
    )
    new_campaign_log = CampaignLogModel(
        campaign_id=campaign_id,
        user_id=current_user.id,
        activity="ADD_MEMBER",
        did_at=datetime.now(timezone.utc)
    )
    db.add_all([new_member, new_campaign_log])
    db.commit()
    db.refresh(new_member)
    db.refresh(new_campaign_log)
    return new_member

def delete_member(campaign_id: int, user_id: int, current_user: UserModel, db: Session):
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
    if campaign_db.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền xóa thành viên"
        )
    member = db.query(CampaignMemberModel).filter(
        CampaignMemberModel.campaign_id == campaign_id,
        CampaignMemberModel.user_id == user_id
    ).first()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Người dùng không thuộc chiến dịch"
        )
    if member.role == "OWNER":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Không thể xóa owner"
        )
    new_campaign_log = CampaignLogModel(
        campaign_id=campaign_id,
        user_id=current_user.id,
        activity="REMOVE_MEMBER",
        did_at=datetime.now(timezone.utc)
    )
    db.delete(member)
    db.add(new_campaign_log)
    db.commit()
    db.refresh(new_campaign_log)
    return

def get_members(campaign_id: int, current_user: UserModel, db: Session):
    campaign_db = (
        db.query(CampaignModel)
        .join(CampaignMemberModel)
        .filter(
            CampaignModel.id == campaign_id,
            CampaignMemberModel.user_id == current_user.id,
            CampaignModel.is_delete.is_(False)
        )
        .first()
    )
    if not campaign_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy chiến dịch hoặc bạn không tham gia"
        )
    return (
        db.query(CampaignMemberModel)
        .options(joinedload(CampaignMemberModel.user))
        .filter(CampaignMemberModel.campaign_id == campaign_id)
        .all()
    )