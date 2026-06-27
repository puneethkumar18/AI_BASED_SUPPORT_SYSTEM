from sqlalchemy.orm import Session
from app.models.ticket_history import TicketHistory

class HistorySevices:

    @staticmethod
    def log_history(
        db:Session,
        action:str,
        ticket_id:int,
        user_id:int,
        old_value:str=None,
        new_value:str=None):

        history = TicketHistory(
            action=action,
            performed_by=user_id,
            ticket_id=ticket_id,
            old_value=old_value,
            new_value = new_value
        )
        db.add(history)
        db.commit()
        db.refresh(history)

        return history
    
    @staticmethod
    def get_history(db:Session,ticket_id:int):
        return (
            db.query(TicketHistory)
            .filter(TicketHistory.ticket_id == ticket_id)
            .order_by(TicketHistory.created_at.asc())
            .all()
        )