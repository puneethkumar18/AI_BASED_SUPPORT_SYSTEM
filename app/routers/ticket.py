from fastapi import APIRouter,status,HTTPException,Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.user import User
from app.auth.dependencies import get_current_user,require_roles
from app.services.ticket_services import TicketServices
from app.schemas.ticket import (TicketResponse,TicketUpdate,TicketCreate,AssignTicket)
from typing import List
from app.core.enums import RoleEnum


router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
    )


@router.post("",response_model=TicketResponse,status_code=status.HTTP_201_CREATED)
async def create_ticket(
    ticket:TicketCreate,
    db:Session = Depends(get_db),
    current_user:User=Depends(require_roles(RoleEnum.ADMIN,RoleEnum.CUSTOMER))):
    return await TicketServices.create_ticket(db,ticket,current_user)

@router.get("/my",response_model=List[TicketResponse])
def get_my_tickets(current_user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    tickets=TicketServices.get_my_tickets(db,current_user)
    return tickets

@router.get("/{ticket_id}",response_model=TicketResponse)
def get_ticket(ticket_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    ticket = TicketServices.get_ticket_by_id(db,ticket_id)

    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="=Ticket not found"
        )

    if ticket.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Denied"
        )
    return ticket

@router.patch("/{ticket_id}",response_model=TicketResponse)
def update_ticket(
    ticket_id:int,
    ticket_data :TicketUpdate,
    db:Session=Depends(get_db),
    current_user:User=Depends(require_roles(RoleEnum.ADMIN,RoleEnum.SUPPORT_AGENT))):

    ticket = TicketServices.get_ticket_by_id(db,ticket_id)

    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket Not Found")
    
    if ticket.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Denied"
        )
    
    return TicketServices.update_ticket(db,ticket,ticket_data,current_user.id)



@router.patch("/{ticket_id}/assign",response_model=TicketResponse)
def assign_ticket(
    ticket_id:int,
    assignment: AssignTicket,
    db:Session=Depends(get_db),
    current_user:User=Depends(require_roles(RoleEnum.ADMIN))
    ):
    ticket = TicketServices.get_ticket_by_id(db,ticket_id)
    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket does not Exists"
        )
    return TicketServices.assign_ticket(db,ticket,assignment.assigned_to,current_user.id)




