

from celery import Celery
from app.core.config import settings

celery = Celery(
    "support_system",
    broker=settings.CELERY_BROKER,
    backend=settings.CELERY_BACKEND)

celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Kolkata",
    enable_utc=False
)