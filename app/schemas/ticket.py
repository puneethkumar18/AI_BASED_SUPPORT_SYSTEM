from pydantic import BaseModel,ConfigDict
from typing import Optional
from app.models.ticket import TicketStatus,TicketPriority

class TicketCreate(BaseModel):
    title:str
    description:str


class TicketResponse(BaseModel):
    id:int
    title:str
    description:str
    category: Optional[str] = None
    summary: Optional[str] = None
    suggested_resolution :Optional[str] = None
    status:TicketStatus
    priority : TicketPriority
    category: Optional[str] = None
    created_by : int
    assigned_to: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class TicketUpdate(BaseModel):
    title:Optional[str] = None
    description:Optional[str] = None
    category:Optional[str] = None
    status:Optional[TicketStatus]= None
    priority  : Optional[TicketPriority] = None
    assiged_to : Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class AssignTicket(BaseModel):
    assigned_to: int