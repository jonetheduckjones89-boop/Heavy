from .celery_app import celery
from app.services.document_processor import extract_text_from_file
from app.services.ai_agent import classify_document, extract_fields, generate_actions, summarize
from app.db import engine
from sqlmodel import Session, select
from app import models, crud
from app.services.storage import make_public_url
import os
import logging

logger = logging.getLogger(__name__)

@celery.task(bind=True, name="process_document")
def process_document(self, document_id: str):
    """
    Celery worker: full pipeline
    """
    with Session(engine) as session:
        doc = session.exec(select(models.Document).where(models.Document.id == document_id)).one_or_none()
        if not doc:
            logger.error("Document not found %s", document_id)
            return {"status":"not_found"}
        try:
            doc.status = "processing"
            session.add(doc); session.commit()

            text = extract_text_from_file(doc.file_path)
            doc.raw_text = text
            cls = celery.backend.redis_client  # avoid linter; placeholder
            # classify
            # run async functions from sync Celery worker using asyncio
            async def run_pipeline(doc_text):
                c = await classify_document(doc_text)
                e = await extract_fields(doc_text)
                a = await generate_actions(e, doc_text)
                s = await summarize(doc_text)
                return c, e, a, s

            import asyncio
            cls_res, extracted, actions, summary = asyncio.run(run_pipeline(text))

            metadata = {"classification": cls_res, "extracted": extracted, "actions": actions, "summary": summary}
            doc.doc_metadata = metadata
            doc.doc_type = cls_res.get("doc_type")
            doc.status = "done"
            session.add(doc); session.commit()

            # Optionally generate a DOCX file here and record generated file
            # omitted for brevity; use app.services.docxGenerator
            return {"status":"done"}
        except Exception as e:
            logger.exception("process_document error")
            doc.status = "error"
            doc.doc_metadata = {"error": str(e)}
            session.add(doc); session.commit()
            raise
