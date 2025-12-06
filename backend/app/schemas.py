from pydantic import BaseModel
from typing import Optional, List, Any

class UploadResponse(BaseModel):
    document_id: str
    filename: str

class DocumentInDB(BaseModel):
    id: str
    filename: str
    status: str
    doc_type: Optional[str]
    doc_metadata: Optional[Any]

class AnalyzeRequest(BaseModel):
    text: str

class GenerateRequest(BaseModel):
    template_name: str = "patient_summary"
