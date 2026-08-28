from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime

class UserInCampaignMemberResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: str

class CampaignMemberResponse(BaseModel):
    campaign_id: int
    role: str
    user: UserInCampaignMemberResponse
    joined_at: datetime
    model_config = ConfigDict(from_attributes=True)