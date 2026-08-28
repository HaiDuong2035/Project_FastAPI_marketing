from sqlalchemy import ForeignKey, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from db.database import Base

class CampaignLogModel(Base):
    __tablename__="campaign_log"
    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    activity = Column(String(20), nullable=False)
    did_at = Column(DateTime, nullable=False)

    user = relationship(
        "UserModel",
        back_populates="campaign_log"
    )

    campaign = relationship(
        "CampaignModel",
        back_populates="campaign_log"
    )