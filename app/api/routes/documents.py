from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, BackgroundTasks
from app.db import get_session
from sqlmodel import Session
from app import crud, models
from app.services.storage import save_bytes, make_public_url
from app.services.document_processor import save_upload_file
from app.tasks.celery_app import celery
from app.tasks.workers import process_document
from app.schemas import UploadResponse
from typing import Any

router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...), patient_id: str | None = None, session: Session = Depends(get_session)):
    # Save file and create DB record
    file_path, preview = await save_upload_file(file)
    d = crud.create_document(session, filename=file.filename, file_path=file_path, patient_id=patient_id)
    # enqueue Celery task
    process_document.apply_async(args=[d.id], queue="documents")
    return {"document_id": d.id, "filename": d.filename}

@router.get("/{document_id}")
def get_document(document_id: str, session: Session = Depends(get_session)):
    doc = crud.get_document(session, document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"document": doc}
