import os
from app.services.storage import save_bytes
import tempfile
from typing import Tuple
from pypdf import PdfReader
import mammoth
from fastapi import UploadFile
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

async def save_upload_file(upload_file: UploadFile) -> Tuple[str, str]:
    """
    Save UploadFile to storage and extract a text preview (for quick processing).
    Returns (file_path, preview_text).
    """
    content = await upload_file.read()
    file_path = save_bytes(content, upload_file.filename)
    text = extract_text_from_file(file_path)
    preview = text[:4000]
    return file_path, preview

def extract_text_from_file(file_path: str) -> str:
    lower = file_path.lower()
    try:
        if lower.endswith(".pdf"):
            reader = PdfReader(file_path)
            pages = [p.extract_text() or "" for p in reader.pages]
            return "\n".join(pages)
        if lower.endswith(".docx") or lower.endswith(".doc"):
            with open(file_path, "rb") as f:
                res = mammoth.extract_raw_text(f)
                return res.value or ""
        # try plain text
        with open(file_path, "rb") as f:
            return f.read().decode("utf-8", errors="ignore")
    except Exception as e:
        logger.exception("extract_text error")
        return ""
