from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship

from db.database import Base

class CampaignTaskCommentModel(Base):
    __tablename__ = "campaign_task_comments"
    id = Column(Integer, primary_key=True)
    campaign_task_id = Column(Integer, ForeignKey("campaign_tasks.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False)

    campaign_task = relationship(
        "CampaignTaskModel",
        back_populates="comments"
    )

    user = relationship(
        "UserModel",
        back_populates="campaign_task_comments"
    )