import os, uuid
from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from core.config import UPLOAD_DIR
from core.config import MAX_FILE_SIZE
from models.user import UserModel
from models.campaign_member import CampaignMemberModel
from models.campaign_task import CampaignTaskModel
from models.campaign_task_attachment import CampaignTaskAttachmentModel

ALLOWED_TYPES = {
    "image/png",
    "image/jpeg",
    "application/pdf"
}

def upload_task_attachment(
    task_id: int,
    file: UploadFile,
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
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Loại file không được hỗ trợ"
        )
    content = file.file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File không được vượt quá 10MB"
        )
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_extension = os.path.splitext(file.filename)[1]
    new_file_name = (f"{uuid.uuid4()}{file_extension}")
    file_path = os.path.join(UPLOAD_DIR,new_file_name)
    with open(file_path, "wb") as buffer:
        buffer.write(content)
    new_attachment = CampaignTaskAttachmentModel(
        task_id=task.id,
        user_id=current_user.id,
        file_name=file.filename,
        file_path=file_path,
        file_size=len(content),
        created_at=datetime.now(timezone.utc)
    )
    db.add(new_attachment)
    db.commit()
    db.refresh(new_attachment)
    return new_attachment