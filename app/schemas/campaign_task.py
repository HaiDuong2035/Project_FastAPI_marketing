from enum import Enum
from pydantic import BaseModel
from datetime import datetime

class TaskStatus(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class TaskPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class SortType(str, Enum):
    CREATED_AT = "CREATED_AT"
    DUE_DATE = "DUE_DATE"

class CampaignTaskCreate(BaseModel):
    title: str
    assignee_id: int = None
    priority: str = "MEDIUM"
    description: str = None
    due_date: datetime

class CampaignTaskUpdate(BaseModel):
    title: str = None
    description: str = None
    assignee_id: int = None
    status: TaskStatus = None
    priority: TaskPriority = None