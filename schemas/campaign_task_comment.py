from pydantic import BaseModel

class CampaignTaskCommentCreate(BaseModel):
    content: str