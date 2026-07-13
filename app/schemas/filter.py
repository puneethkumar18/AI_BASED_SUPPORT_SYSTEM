from pydantic import BaseModel
from typing import Optional
from app.core.enums import TicketStatus
from app.core.enums import TicketPriority

from app.schemas.ticket import TicketResponse


class TicketSearchResponse(BaseModel):
    total: int
    page: int
    size: int
    items: list[TicketResponse]

class TicketFilter(BaseModel):
    page:int=1
    size:int=10
    search: Optional[str] = None
    status: Optional[TicketStatus] = None
    priority: Optional[TicketPriority] = None
    category: Optional[str] = None
    assigned_to: Optional[int] = None
    created_by: Optional[int] = None
    sort_by: str = "created_at"
    sort_order: str = "desc"
    