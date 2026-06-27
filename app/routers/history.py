from fastapi import APIRouter,Depends
from app.schemas.history import HistoryResponse
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.services.history_service import HistorySevices
from app.models.user import User
from app.auth.dependencies import get_current_user

router = APIRouter(
    prefix="/tickets",
    tags=["ticket_history"]
)


@router.get("/{ticket_id}/history",response_model= List[HistoryResponse])
def ticket_history(ticket_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    logs = HistorySevices.get_history(db,ticket_id)
    return logs