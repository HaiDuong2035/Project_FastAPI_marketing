from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from db.database import Base

class CampaignTaskModel(Base):
    __tablename__="campaign_tasks"
    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
    title = Column(String(50), nullable=False)
    description = Column(Text)
    assignee_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String(15), nullable=False)
    priority = Column(String(10), nullable=False)
    due_date = Column(DateTime)
    created_at = Column(DateTime, nullable=False)
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    assignee = relationship(
        "UserModel",
        back_populates="campaign_tasks"
    )

    campaign = relationship(
        "CampaignModel",
        back_populates="campaign_tasks"
    )

    comments = relationship(
        "CampaignTaskCommentModel",
        back_populates="campaign_task"
    )

    attachments = relationship(
        "CampaignTaskAttachmentModel",
        back_populates="campaign_task"
    )

    creator = relationship(
        "UserModel",
        back_populates="created_campaign_task"
    )