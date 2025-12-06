from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid

def gen_uuid() -> str:
    return str(uuid.uuid4())

class Patient(SQLModel, table=True):
    id: str = Field(default_factory=gen_uuid, primary_key=True)
    clinic_id: Optional[str] = None
    name: Optional[str] = None
    dob: Optional[str] = None
    gender: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Document(SQLModel, table=True):
    id: str = Field(default_factory=gen_uuid, primary_key=True)
    patient_id: Optional[str] = Field(default=None, foreign_key="patient.id")
    clinic_id: Optional[str] = None
    filename: str
    file_path: str
    uploaded_by: Optional[str] = None
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(default="uploaded")  # uploaded, processing, done, error
    doc_type: Optional[str] = None
    raw_text: Optional[str] = None
    doc_metadata: Optional[dict] = Field(default=None, sa_column_kwargs={"name": "doc_metadata"})  # extracted fields, actions, summary
    processed_at: Optional[datetime] = None

class GeneratedFile(SQLModel, table=True):
    id: str = Field(default_factory=gen_uuid, primary_key=True)
    document_id: Optional[str] = Field(default=None, foreign_key="document.id")
    patient_id: Optional[str] = Field(default=None, foreign_key="patient.id")
    filename: str
    file_path: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
