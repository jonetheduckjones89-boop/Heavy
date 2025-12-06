from sqlmodel import Session, select
from app import models
from typing import Optional
from datetime import datetime

def create_patient(session: Session, name: str, dob: Optional[str] = None, gender: Optional[str] = None) -> models.Patient:
    p = models.Patient(name=name, dob=dob, gender=gender)
    session.add(p)
    session.commit()
    session.refresh(p)
    return p

def create_document(session: Session, filename: str, file_path: str, patient_id: Optional[str] = None, clinic_id: Optional[str] = None, uploaded_by: Optional[str] = None) -> models.Document:
    d = models.Document(filename=filename, file_path=file_path, patient_id=patient_id, clinic_id=clinic_id, uploaded_by=uploaded_by)
    session.add(d)
    session.commit()
    session.refresh(d)
    return d

def get_document(session: Session, document_id: str) -> Optional[models.Document]:
    return session.get(models.Document, document_id)

def update_document_processed(session: Session, document: models.Document, doc_metadata: dict):
    document.doc_metadata = doc_metadata
    document.status = "done"
    document.processed_at = datetime.utcnow()
    session.add(document)
    session.commit()
    session.refresh(document)
    return document

def create_generated(session: Session, document_id: str, patient_id: Optional[str], filename: str, file_path: str):
    g = models.GeneratedFile(document_id=document_id, patient_id=patient_id, filename=filename, file_path=file_path)
    session.add(g)
    session.commit()
    session.refresh(g)
    return g
