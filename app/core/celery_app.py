

from celery import Celery
from app.core.config import settings

from app.models.user import User
from app.models.ticket import Ticket
from app.models.ticket_history import TicketHistory
from app.models.comment import Comment
from app.models.attachment import Attachment

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

# celery.autodiscover_tasks([
#     "app.core.tasks",
# ])

celery.conf.imports = (
    "app.core.tasks.email_tasks",
    "app.core.tasks.logging_tasks",
)