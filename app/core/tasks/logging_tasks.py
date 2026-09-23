from app.core.celery_app import celery

from app.services.history_service import HistorySevices
from app.database.database import SessionLocal

@celery.task
def log_ticket_created(
    action,
    user_id,
    ticket_id,
    new_value
    ):
    db = SessionLocal()
    HistorySevices.log_history(
        db=db,
        action=action,
        user_id=user_id,
        ticket_id=ticket_id,
        new_value=new_value
    )