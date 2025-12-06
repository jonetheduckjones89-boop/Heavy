# Lightweight meeting scheduler stub - integrate Google Calendar / MS Graph later
from typing import Dict
import logging
logger = logging.getLogger(__name__)

def schedule_meeting(patient_email: str, start_ts: str, duration_minutes: int, summary: str) -> Dict:
    # Implement OAuth2 flow + create event via Google Calendar API.
    logger.info("Meeting scheduled (stub) for %s at %s", patient_email, start_ts)
    return {"status":"scheduled","id":"stub-event-id"}
