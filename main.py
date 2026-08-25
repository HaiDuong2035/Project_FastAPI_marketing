from fastapi import FastAPI, Request, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from db.database import Base, engine
from core.exceptions import create_response

from routers.auth import router as auth_router
from routers.user import router as user_router
from routers.campaign import router as campaign_router

from models.user import UserModel
from models.campaign import CampaignModel
from models.campaign_member import CampaignMemberModel
from models.campaign_log import CampaignLogModel
from models.campaign_task import CampaignTaskModel
from models.campaign_task_attachment import CampaignTaskAttachmentModel
from models.campaign_task_comment import CampaignTaskCommentModel

Base.metadata.create_all(bind=engine)

app = FastAPI(title="MARKETING CAMPAIGN MANAGEMENT API")

@app.exception_handler(HTTPException)
def http_exeption_handler(request: Request, exc: HTTPException):
    response = create_response(exc.status_code, "Lỗi", request, error = exc.detail)
    return JSONResponse(response.model_dump(), exc.status_code)

@app.exception_handler(Exception)
def global_exeption_handler (request: Request, exc: Exception):
    response = create_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Lỗi máy chủ", request, error = str(exc))
    return JSONResponse(response.model_dump(), status.HTTP_500_INTERNAL_SERVER_ERROR)

@app.exception_handler(RequestValidationError)
def validation_exception_handler(req: Request, exc: RequestValidationError):
    response = create_response(status.HTTP_422_UNPROCESSABLE_CONTENT, "Lỗi chuẩn hóa nội dung", req, er = exc.errors)
    return JSONResponse(
        content = response.model_dump(),
        status_code = status.HTTP_422_UNPROCESSABLE_CONTENT
    )

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(campaign_router)