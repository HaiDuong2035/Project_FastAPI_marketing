from pydantic import BaseModel, ConfigDict
from datetime import datetime

class CampaignTaskCommentCreate(BaseModel):
    content: str

class CampaignTaskCommentResponse(BaseModel):
    id: int
    content: str
    created_at: datetime
    user_id: int
    model_config = ConfigDict(from_attributes=True)