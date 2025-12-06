from fastapi import APIRouter
from app.db import engine
from sqlmodel import text

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/ready")
def ready():
    return {"status":"ok"}
