from sqlalchemy import ForeignKey, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from db.database import Base

class CampaignMemberModel(Base):
    __tablename__="campaign_members"
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    role = Column(String(10), nullable=False)
    joined_at = Column(DateTime, nullable=False)

    user = relationship(
        "UserModel",
        back_populates="campaign_members"
    )

    campaign = relationship(
        "CampaignModel",
        back_populates="campaign_members"
    )