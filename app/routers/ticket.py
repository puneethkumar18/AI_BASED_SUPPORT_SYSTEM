from fastapi import APIRouter,status,HTTPException,Depends,BackgroundTasks
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.user import User
from app.auth.dependencies import get_current_user,require_roles
from app.services.ticket_services import TicketServices
from app.schemas.ticket import (TicketResponse,TicketUpdate,TicketCreate,AssignTicket,TicketStatusUpdate)
from typing import List
from app.core.enums import RoleEnum
from app.services.user_services import UserService

from app.exceptions.custom_exception import *


router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
    )


@router.post("",response_model=TicketResponse,status_code=status.HTTP_201_CREATED)
async def create_ticket(
    ticket:TicketCreate,
    background_tasks: BackgroundTasks,
    db:Session = Depends(get_db),
    current_user:User=Depends(require_roles(RoleEnum.ADMIN,RoleEnum.CUSTOMER,RoleEnum.SUPPORT_AGENT))):
    return await TicketServices.create_ticket(db,ticket,current_user,background_tasks)

@router.get("",response_model=List[TicketResponse])
def get_all_tickets(
    db:Session=Depends(get_db),
    current_user:User=Depends(require_roles(RoleEnum.ADMIN,RoleEnum.CUSTOMER,RoleEnum.SUPPORT_AGENT))
    ):
    return TicketServices.get_all_tickets(db)

@router.get("/my",response_model=List[TicketResponse])
def get_my_tickets(
    db:Session=Depends(get_db),
    current_user:User=Depends(require_roles(RoleEnum.CUSTOMER,RoleEnum.ADMIN,RoleEnum.SUPPORT_AGENT))
    ):
    tickets=TicketServices.get_my_tickets(db,current_user)
    return tickets

@router.get("/{ticket_id}",response_model=TicketResponse)
def get_ticket(
    ticket_id:int,
    db:Session=Depends(get_db),
    current_user:User=Depends(require_roles(RoleEnum.ADMIN,RoleEnum.SUPPORT_AGENT))
    ):
    ticket = TicketServices.get_ticket_by_id(db,ticket_id)

    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
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
    current_user:User=Depends(get_current_user)):

    ticket = TicketServices.get_ticket_by_id(db,ticket_id)

    if ticket is None:
        raise TicketNotFoundException()
    
    
    return TicketServices.update_ticket(db,ticket,ticket_data,current_user)


@router.patch("/{ticket_id}/status",response_model=TicketResponse)
def update_ticket_status(
    ticket_id:int,
    status_data:TicketStatusUpdate,
    background_tasks: BackgroundTasks,
    db:Session=Depends(get_db),
    current_user:User=Depends(require_roles(RoleEnum.ADMIN,RoleEnum.SUPPORT_AGENT))    
    ):

    allowed = {
        "OPEN":["IN_PROGRESS","RESOLVED"],
        "IN_PROGRESS":["RESOLVED"],
        "RESOLVED":["CLOSED"]
    }
    ticket = TicketServices.get_ticket_by_id(db,ticket_id)
    if ticket is None:
        raise TicketNotFoundException

    if ticket.assigned_to is None:
        raise ValueErrorException(f"Ticket {ticket_id} has not been assigned to any one so kindly please assign the Ticket")

    if status_data.status not in allowed[ticket.status]:
        raise ValueErrorException(f"Cannot Move Status from {ticket.status.name} to {status_data.status.name}")
    
    return TicketServices.update_ticket_status(
        db=db,
        ticket=ticket,
        new_status=status_data.status.name,
        current_user=current_user,
        background_tasks= background_tasks
    )


@router.patch("/{ticket_id}/assign",response_model=TicketResponse)
async def assign_ticket(
    ticket_id:int,
    assignment: AssignTicket,
    db:Session=Depends(get_db),
    current_user:User=Depends(require_roles(RoleEnum.ADMIN))
    ):
    ticket = TicketServices.get_ticket_by_id(db,ticket_id)
    if ticket is None:
        raise TicketNotFoundException

    return await TicketServices.assign_ticket(db,ticket,assignment.assigned_to,current_user.id)




