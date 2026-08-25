from sqlalchemy import Column, String, Integer, Boolean, DateTime
from sqlalchemy.orm import relationship
from db.database import Base

class UserModel(Base):
    __tablename__="users"
    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(String(10), default="USER")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, nullable=False)

    campaigns = relationship(
        "CampaignModel",
        back_populates="owner"
    )

    campaign_members = relationship(
        "CampaignMemberModel",
        back_populates="user"
    )

    campaign_tasks = relationship(
        "CampaignTaskModel",
        back_populates="assignee"
    )

    campaign_log = relationship(
        "CampaignLogModel",
        back_populates="user"
    )

    campaign_task_comments = relationship(
        "CampaignTaskCommentModel",
        back_populates="user"
    )

    campaign_task_attachments = relationship(
        "CampaignTaskAttachmentModel",
        back_populates="user"
    )

    created_campaign_task = relationship(
        "CampaignTaskModel",
        back_populates="creator"
    )