from fastapi import Request
from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime, timezone

class BaseResponse(BaseModel):
    status_code: int
    message: str
    data: Optional[Any]
    error: Optional[str]
    time_stamp: str
    path: str

def create_response(status_code: int, message: str, request: Request, data = None, error = None):
    return BaseResponse(
        status_code = status_code,
        message = message,
        data = data,
        error = error,
        time_stamp = datetime.now(timezone.utc).isoformat(),
        path = request.url.path
    )