from fastapi import APIRouter,Depends,HTTPException,status
from app.schemas.comment import CommentResponse
from sqlalchemy.orm import Session
from app.core.enums import RoleEnum
from app.auth.dependencies import require_roles,get_current_user
from app.database.database import get_db
from app.schemas.comment import CommentCreate
from app.services.comment_services import CommentServices
from app.services.ticket_services import TicketServices
from typing import List
from fastapi import BackgroundTasks


router = APIRouter(prefix="/tickets",tags=["Comments"])

@router.post("/{ticket_id}/comments",response_model=CommentResponse)
def add_comment(
    ticket_id:int,
    comment_data:CommentCreate,
    background_tasks:BackgroundTasks,
    db:Session = Depends(get_db),
    current_user = Depends(get_current_user)):

    ticket = TicketServices.get_ticket_by_id(db,ticket_id)
    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket is not Found"
        )
    comment = CommentServices.add_comment(
        db,ticket,
        current_user,
        comment_data,
        background_tasks=background_tasks
        )

    return comment

@router.get("/{ticket_id}/comments",response_model= List[CommentResponse])
def get_comments(
    ticket_id:int,
    db:Session = Depends(get_db),
    current_user = Depends(get_current_user)):

    ticket = TicketServices.get_ticket_by_id(db,ticket_id)
    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket is not Found"
        )
    
    comments = CommentServices.get_comments(db,ticket_id)
    
    return comments

@router.delete("/comments/{comment_id}")
def delete_comment(
    comment_id:int,
    db:Session=Depends(get_db),
    current_user = Depends(get_current_user)):
    return CommentServices.delete_comment(db,comment_id)
