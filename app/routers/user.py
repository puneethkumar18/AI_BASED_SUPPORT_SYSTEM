

from fastapi import APIRouter,Depends
from app.schemas.user import UserResponse
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.user import User
from typing import List

router = APIRouter(prefix="/users",tags=["Users"])


@router.get("",response_model=List[UserResponse])
def get_all_users(db:Session=Depends(get_db)):
    return db.query(User).all()