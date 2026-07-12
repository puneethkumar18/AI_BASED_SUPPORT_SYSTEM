from sqlalchemy.orm import Session
from app.models.ticket import Ticket
from app.core.enums import TicketStatus
from sqlalchemy import func
from app.models.user import User


class DashboardService:

    @staticmethod
    def get_summery(db:Session):
        return {
            "total_tickets":db.query(Ticket).count(),
            "open_tickets":db.query(Ticket).filter(Ticket.status == TicketStatus.OPEN).count(),
            "in_progress":db.query(Ticket).filter(Ticket.status == TicketStatus.IN_PROGRESS).count(),
            "closed":db.query(Ticket).filter(Ticket.status == TicketStatus.CLOSED).count()
        }
    

    @staticmethod
    def priority_statistics(db:Session):
        result = db.query(Ticket.priority,func.count(Ticket.id)).group_by(Ticket.priority).all()
        return [
            {
                "priority":priority.value,
                "count":count
            }
            for priority,count in result
        ]
    

    @staticmethod
    def category_statistics(db:Session):
        result = db.query(Ticket.category,func.count(Ticket.id)).group_by(Ticket.category).all()

        return [
            {
                "category":category,
                "count":count
            }
            for category,count in result
        ]
    
    @staticmethod
    def agent_performance(db:Session):
        result = db.query(
                User.id,
                User.name,
                func.count(Ticket.id)).join(
                    Ticket,Ticket.assiged_to == User.id).group_by(User.id,User.name).all()
        
        data = []

        for agent_id,name,assigned in result:
            closed = (db.query(Ticket)
                        .filter(
                            Ticket.assiged_to == agent_id,
                            Ticket.status == TicketStatus.CLOSED)
                        ).count()
            
            data.append({
                "agent_id":agent_id,
                "agent_name":name,
                "assigned":assigned,
                "closed":closed
            })

        return data