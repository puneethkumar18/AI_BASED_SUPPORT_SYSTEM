from sqlalchemy import Column,Integer,String,DateTime
from sqlalchemy.sql import func
from app.database.database import Base
from enum import Enum
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import relationship

from app.core.enums import RoleEnum

class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(100),nullable=False)
    email = Column(String(255),nullable=False,unique=True)
    password_hash = Column(String(255),nullable=False)
    role = Column(SqlEnum(RoleEnum),default=RoleEnum.CUSTOMER,nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    created_tickets = relationship("Ticket",foreign_keys="Ticket.created_by",back_populates="creator")

    
    