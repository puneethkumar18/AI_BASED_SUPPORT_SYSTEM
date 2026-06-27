from app.auth.hashing import hash_password,verify_password
from app.models.user import User
from app.schemas.user import UserRegister,UserLogin
from sqlalchemy.orm import Session

class UserService:

    @staticmethod
    def get_user_by_email(db:Session,email:str):
        return (db.query(User).filter(User.email == email).first())
    
    @staticmethod
    def create_user(db:Session,user_data: UserRegister):
        existing_user = (
            UserService.get_user_by_email(db,user_data.email)
        )

        if existing_user:
            return None
        
        hashed_password = hash_password(
            user_data.password
        )

        user = User(
            name = user_data.name,
            email = user_data.email,
            password_hash = hashed_password,
            role = user_data.role
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user
    
    @staticmethod
    def authenticate_user(db:Session,email:str,password:str):
        user = UserService.get_user_by_email(db,email)
        if not user:
            return None
        if not verify_password(password,user.password_hash):
            return None

        return user
