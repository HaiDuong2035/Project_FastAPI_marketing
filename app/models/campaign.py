from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from db.database import Base

class CampaignModel(Base):
    __tablename__="campaigns"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, nullable=False)
    is_delete = Column(Boolean, default=False)

    owner = relationship(
        "UserModel",
        back_populates="campaigns"
    )

    campaign_members = relationship(
        "CampaignMemberModel",
        back_populates="campaign"
    )

    campaign_tasks = relationship(
        "CampaignTaskModel",
        back_populates="campaign"
    )

    campaign_log = relationship(
        "CampaignLogModel",
        back_populates="campaign"
    )