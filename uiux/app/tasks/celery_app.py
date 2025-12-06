from celery import Celery
from app.core.config import settings

celery = Celery(
    "medcore",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

# Optional: load celery config from env
celery.conf.update(task_track_started=True, worker_prefetch_multiplier=1, task_acks_late=True)
