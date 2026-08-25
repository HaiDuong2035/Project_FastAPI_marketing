from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship

from db.database import Base

class CampaignTaskAttachmentModel(Base):
    __tablename__ = "campaign_task_attachments"
    id = Column(Integer, primary_key=True)
    campaign_task_id = Column(Integer, ForeignKey("campaign_tasks.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    path = Column(String(500), nullable=False)
    size = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)

    campaign_task = relationship(
        "CampaignTaskModel",
        back_populates="attachments"
    )

    user = relationship(
        "UserModel",
        back_populates="campaign_task_attachments"
    )