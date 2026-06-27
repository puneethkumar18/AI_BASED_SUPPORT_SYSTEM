from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from app.schemas.user import UserResponse,UserRegister,UserLogin,Token
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.auth.dependencies import get_current_user
from app.services.user_services import UserService
from app.auth.jwt_handler import create_access_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register",response_model=UserResponse)
def register_user(user:UserRegister,db:Session = Depends(get_db)):
    create_user =  UserService.create_user(db=db,user_data=user)
    if not create_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )
    return create_user

@router.post("/login",response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(),db:Session=Depends(get_db)):
    authanticate_user = (
        UserService.authenticate_user(
            db,form_data.username,form_data.password
        )
    )
    if authanticate_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    token = create_access_token(
        {
            "sub":authanticate_user.email,
            "user_id":authanticate_user.id,
            "role":authanticate_user.role
        }
    )
    return {
        "access_token" : token,
        "token_type":"bearer"
    }


@router.get("/me",response_model=UserResponse)
def current_user(user = Depends(get_current_user)):
    return user