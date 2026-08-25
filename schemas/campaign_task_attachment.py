from pydantic import BaseModel, ConfigDict
from datetime import datetime

class CampaignTaskAttachmentResponse(BaseModel):
    id: int
    file_name: str
    file_path: str
    file_size: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)