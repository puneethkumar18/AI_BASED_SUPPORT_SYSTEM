from app.database.database import Base
from sqlalchemy import INTEGER,Column,ForeignKey,DateTime,String,Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class TicketHistory(Base):
    __tablename__ = "ticket_history"

    id = Column(INTEGER,primary_key=True,index=True)
    old_value = Column(Text,nullable=True)
    new_value = Column(Text,nullable=True)
    action = Column(String,nullable=False)
    ticket_id = Column(INTEGER,ForeignKey("tickets.id"),nullable=False)
    performed_by = Column(INTEGER,ForeignKey("users.id"),nullable=False)
    created_at = Column(DateTime(timezone=True),server_default=func.now())
    
    ticket = relationship("Ticket",back_populates="history")
    user = relationship("User")