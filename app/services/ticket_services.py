from app.schemas.ticket import TicketCreate,TicketUpdate
from sqlalchemy.orm import Session 
from app.models.user import User
from app.services.ai_sevices import AIServices
from app.services.history_service import HistorySevices
from app.models.ticket import Ticket
from app.core.enums import RoleEnum

class TicketServices:

    @staticmethod
    def create_ticket(db:Session,ticket_data:TicketCreate,current_user:User):
        # ticket = Ticket(
        #     title=ticket_data.title,
        #     description = ticket_data.description,
        #     created_by = current_user.id
        # )
        analysis = AIServices.analyze_ticket(ticket_data.title,ticket_data.description)
        ticket = Ticket(
            **ticket_data.model_dump(),
            category=analysis["category"],
            priority=analysis["priority"],
            summary=analysis["summary"],
            suggested_resolution=analysis["suggested_resolution"],
            created_by = current_user.id
        )
        
        db.add(ticket)
        db.commit()
        db.refresh(ticket)

        HistorySevices.log_history(
            db=db,
            action="TICKET CREATED",
            user_id=current_user.id,
            ticket_id=ticket.id,
            new_value= ticket.title
        )
        return ticket

    @staticmethod
    def get_ticket_by_id(db:Session,ticket_id:int):
        ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
        return ticket

    @staticmethod
    def get_my_tickets(db:Session,current_user:User):
        tickets = db.query(Ticket).filter(Ticket.created_by == current_user.id).all()
        return tickets

    @staticmethod
    def update_ticket(db:Session,ticket:Ticket,ticket_data:TicketUpdate,current_user_id:int):
        old_status = ticket.status
        update_data = ticket_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(ticket, key, value)

        db.commit()
        db.refresh(ticket)
        # STATUS CHANGES LOGS
        if old_status != ticket.status:
            HistorySevices.log_history(
            db=db,
            user_id=current_user_id,
            ticket_id=ticket.id,
            action="STATUS CHANGED",
            old_value=old_status,
            new_value=ticket.status
            )
        return ticket
    
    @staticmethod
    def assign_ticket(db:Session,ticket: Ticket,assigned_user_id: int,current_user_id:int):
        agent = (db.query(User).filter(User.id == assigned_user_id).first())
        if agent is None:
            raise ValueError("Support agent not found.")
        if agent.role != RoleEnum.SUPPORT_AGENT:
            raise ValueError("User is not a support agent.")
        
        ticket.assigned_to = agent.id
        db.commit()
        db.refresh(ticket)

        HistorySevices.log_history(
            db=db,
            action="TICKET ASSIGNED",
            ticket_id=ticket.id,
            user_id=current_user_id,
            old_value=str(ticket.assiged_to),
            new_value=str(agent.id)
        )
        return ticket
