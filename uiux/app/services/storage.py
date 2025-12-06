import os
from pathlib import Path
from uuid import uuid4
from app.core.config import settings

def ensure_storage():
    Path(settings.storage_dir).mkdir(parents=True, exist_ok=True)

def save_bytes(data: bytes, original_name: str) -> str:
    ensure_storage()
    uid = uuid4().hex
    safe = original_name.replace(" ", "_")[:100]
    out = os.path.join(settings.storage_dir, f"{uid}_{safe}")
    with open(out, "wb") as f:
        f.write(data)
    return out

def make_public_url(file_path: str) -> str:
    # For MVP we return path. In production return signed S3 or CDN URL.
    return file_path
