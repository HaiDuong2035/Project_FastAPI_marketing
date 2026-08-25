from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime

class CampaignCreate(BaseModel):
    name: str
    description: str

class CampaignUpdate(BaseModel):
    name: str = None
    description: str = None

class UserInCampaignResponse(BaseModel):
    full_name: str
    email: EmailStr
    role: str
    is_active: bool
    model_config = ConfigDict(from_attributes=True)

class CampaignResponse(BaseModel):
    id: int
    name: str
    description: str
    owner: UserInCampaignResponse
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)