from fastapi import HTTPException,Depends,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.auth.jwt_handler import decode_access_token
from app.models.user import User
from app.core.enums import RoleEnum
from app.database.database import get_db


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

def require_roles(*roles:RoleEnum):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(
                status_code=403,
                detail="Permission denied")
        return current_user
    
    return role_checker

def get_current_user(token:str = Depends(oauth2_scheme),db:Session=Depends(get_db)):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Or Expired token")
    user = (
        db.query(User)
        .filter(User.id == payload["user_id"])
        .first())
    if user == None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not Found")
    return user
