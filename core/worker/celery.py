from celery import Celery

from core.config import settings

celery = Celery(
    "stockflow",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["core.worker.tasks"],
)
