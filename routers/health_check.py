from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "message": "FastAPI đã hoạt động"
    }