from sqlalchemy import or_

from sqlalchemy.orm import Session
from app.models.ticket import Ticket
from app.schemas.filter import TicketFilter

class SearchService:

    @staticmethod
    def search_tickets(
        db: Session,
        filters: TicketFilter
    ):
        query = db.query(Ticket)

        if filters.search:
            query = query.filter(
                or_(
                    Ticket.title.ilike(
                        f"%{filters.search}%"
                    ),
                    Ticket.description.ilike(
                        f"%{filters.search}%"
                    )
                )
            )
        if filters.priority:
            query = query.filter(
                Ticket.priority == filters.priority
            )

        if filters.category:
            query = query.filter(
                Ticket.category == filters.category
            )

        if filters.assigned_to:
            query = query.filter(
                Ticket.assigned_to == filters.assigned_to
            )
        if filters.created_by:
            query = query.filter(
                Ticket.created_by == filters.created_by
            )
        sort_column = getattr(
            Ticket,
            filters.sort_by,
            Ticket.created_at
        )
        if filters.sort_order == "desc":
            query = query.order_by(
                sort_column.desc()
            )
        else:
            query = query.order_by(
                sort_column.asc()
            )

        total = query.count()

        tickets = (
            query
            .offset(
                (filters.page - 1) * filters.size
            )
            .limit(filters.size)
            .all()
        )
        return {
            "total": total,
            "page": filters.page,
            "size": filters.size,
            "items": tickets
        }