from fastapi import APIRouter, Depends
from app.db import get_session
from sqlmodel import Session, select
from app import crud, models
from app.schemas import UploadResponse

router = APIRouter(prefix="/patients", tags=["patients"])

@router.get("")
def list_patients(session: Session = Depends(get_session)):
    patients = session.exec(select(models.Patient)).all()
    return {"patients": patients}
