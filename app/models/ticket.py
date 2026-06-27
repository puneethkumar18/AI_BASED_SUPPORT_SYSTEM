from sqlalchemy import Integer,String,DateTime,Column,ForeignKey
from sqlalchemy.sql import func
from sqlalchemy import Enum as SqlEnum
from enum import Enum
from app.database.database import Base
from sqlalchemy.orm import relationship
from app.core.enums import TicketPriority,TicketStatus


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer,primary_key=True,index=True)
    title = Column(String(40),nullable=False)
    description = Column(String(255),nullable=False)
    summary = Column(String, nullable=True)
    suggested_resolution = Column(String, nullable=True)
    status = Column(SqlEnum(TicketStatus),default=TicketStatus.OPEN,nullable=False)
    priority = Column(SqlEnum(TicketPriority),default=TicketPriority.MEDIUM,nullable=False)
    category = Column(String(20),nullable=True)
    created_by = Column(Integer,ForeignKey("users.id"),nullable=False)
    assiged_to = Column(Integer,ForeignKey("users.id"),nullable=True)
    created_at = Column(DateTime(timezone=True),server_default=func.now())
    updated_at = Column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now())
    
    creator = relationship("User",foreign_keys=[created_by],back_populates="created_tickets")
    assignee = relationship("User",foreign_keys=[assiged_to])
    comments = relationship("Comment",back_populates="ticket",cascade="all, delete-orphan")
    history = relationship("TicketHistory",back_populates="ticket",cascade="all, delete-orphan")
    