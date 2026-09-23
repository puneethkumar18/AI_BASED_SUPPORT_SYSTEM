from app.schemas.ticket import TicketCreate,TicketUpdate
from sqlalchemy.orm import Session 
from app.models.user import User
from app.services.ai_sevices import AIServices
from app.services.history_service import HistorySevices
from app.services.email_services import EmailServices
from app.models.ticket import Ticket
from app.core.enums import RoleEnum
from app.core.logger import logger
from fastapi import BackgroundTasks
from app.services.cache_services import CacheService
from app.exceptions.custom_exception import ValueErrorException
from app.core.tasks.email_tasks import send_ticket_created_email
from app.core.tasks.logging_tasks import log_ticket_created

class TicketServices:

    @staticmethod
    async def create_ticket(
        db:Session,
        ticket_data:TicketCreate,
        current_user:User,
        background_tasks: BackgroundTasks):
        # ticket = Ticket(
        #     title=ticket_data.title,
        #     description = ticket_data.description,
        #     created_by = current_user.id
        # )
        analysis = await AIServices.analyze_ticket(ticket_data.title,ticket_data.description)

        ticket = Ticket(
            **ticket_data.model_dump(),
            category=analysis.category,
            priority=analysis.priority,
            summary=analysis.summary,
            suggested_resolution=analysis.suggested_resolution,
            created_by = current_user.id
        )

        db.add(ticket)
        db.commit()
        db.refresh(ticket)
        CacheService.delete("dashboard_summary")
        background_tasks.add_task(
            logger.info,
            "AI categorized ticket %s as %s",
            ticket.id,
            ticket.category
        )

        send_ticket_created_email.delay(
            current_user.email,
             "Ticket Created Successfully",
                f"""
                    <h2>Ticket Created</h2>
                    Ticket #{ticket.id}
                    Title : {ticket.title}
                    Description : {ticket.description}
                    Status : {ticket.status}
                """
        )
        # background_tasks.add_task(
        #     EmailServices.send_email,
        #     current_user.email,
        #     "Ticket Created Successfully",
        #     f"""
        #         <h2>Ticket Created</h2>
        #         Ticket #{ticket.id}
        #         Title : {ticket.title}
        #         Status : {ticket.status}
        #         """
        # )
        # logger.info(
        #     "AI categorized ticket %s as %s",
        #     ticket.id,
        #     ticket.category
        # )
        # await EmailServices.send_mail(
        #     recipient="puneethkumarg96@gmail.com",
        #     subject="Ticket Created Successfully",
        #     body=f"""
        #         <h2>Ticket Created</h2>
        #         Ticket #{ticket.id}
        #         Title : {ticket.title}
        #         Status : {ticket.status}
        #         """
        # )
        background_tasks.add_task(
            logger.info,
            "Ticket %s created by user %s",
            ticket.id,
            current_user.id,
        )
        # logger.info(
        #     "Ticket %s created by user %s",
        #     ticket.id,
        #     current_user.id
        # )
        # HistorySevices.log_history(
        #     db=db,
        #     action="TICKET CREATED",
        #     user_id=current_user.id,
        #     ticket_id=ticket.id,
        #     new_value= ticket.title
        #)
        log_ticket_created.delay(
            "TICKET CREATED",
            current_user.id,
            ticket.id,
            ticket.title
        )
        # background_tasks.add_task(
        #     HistorySevices.log_history,
        #     db=db,
        #     action="TICKET CREATED",
        #     user_id=current_user.id,
        #     ticket_id=ticket.id,
        #     new_value= ticket.title
        # )
        return ticket

    @staticmethod
    def get_all_tickets(db:Session):
        return db.query(Ticket).order_by(Ticket.id).all()
    @staticmethod
    def get_ticket_by_id(db:Session,ticket_id:int):
        ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
        return ticket

    @staticmethod
    def get_my_tickets(db:Session,current_user:User):
        tickets = db.query(Ticket).filter(Ticket.created_by == current_user.id).all()
        return tickets

    @staticmethod
    def update_ticket_status(
        db:Session,
        ticket:Ticket,
        new_status:str,
        current_user:User,
        background_tasks:BackgroundTasks
        ):
        old_status = ticket.status
        if old_status == new_status:
            raise ValueErrorException("please check the status you are setting the same status again!")
        ticket.status = new_status

        db.commit()
        db.refresh(ticket)
        HistorySevices.log_history(
            db=db,
            action="STATUS CHANGED",
            user_id=current_user.id,
            old_value=old_status,
            new_value=new_status,
            ticket_id=ticket.id
        )

        background_tasks.add_task(
            EmailServices.send_email,
            recipient=current_user.email,
            subject="Ticket Status Updated",
            body= f"""
                    Ticket #{ticket.id}
                    Status changed to
                    {ticket.status}
                """
        )
        return ticket
    @staticmethod
    def update_ticket(db:Session,ticket:Ticket,ticket_data:TicketUpdate,current_user:User):
        update_data = ticket_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(ticket, key, value)

        db.commit()
        db.refresh(ticket)
        CacheService.delete("dashboard_summary")
        # STATUS CHANGES LOGS
        # if old_status != ticket.status:
        #     HistorySevices.log_history(
        #     db=db,
        #     user_id=current_user.id,
        #     ticket_id=ticket.id,
        #     action="STATUS CHANGED",
        #     old_value=old_status,
        #     new_value=ticket.status
        #     )
        #     
        return ticket
    
    @staticmethod
    async def assign_ticket(db:Session,ticket: Ticket,assigned_user_id: int,current_user_id:int):
        agent = (db.query(User).filter(User.id == assigned_user_id).first())
        if agent is None:
            raise ValueErrorException("Support agent not found.")
        if agent.role != RoleEnum.SUPPORT_AGENT:
            raise ValueErrorException("User is not a support agent.")

        if ticket.assigned_to == agent.id:
            raise ValueErrorException("You are assinging to the same user, please check once again")
        
        ticket.assigned_to = agent.id
        db.commit()
        db.refresh(ticket)

        HistorySevices.log_history(
            db=db,
            action="TICKET ASSIGNED",
            ticket_id=ticket.id,
            user_id=current_user_id,
            old_value=str(ticket.assigned_to),
            new_value=str(agent.id)
        )

        send_ticket_created_email.delay(
            recipient=agent.email,
            subject="New Ticket Assigned",
            body=f"""
                Ticket #{ticket.id}
                has been assigned to you.
                """
        )
        return ticket
