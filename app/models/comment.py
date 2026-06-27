from sqlalchemy import Integer,DateTime,Column,ForeignKey,Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.database import Base

class Comment(Base):
    __tablename__  = "comments"

    id = Column(Integer,primary_key=True,index=True)
    message = Column(Text,nullable=False)
    ticket_id = Column(Integer,ForeignKey("tickets.id"),nullable=False)
    user_id = Column(Integer,ForeignKey("users.id"),nullable=False)
    created_at = Column(DateTime(timezone=True),server_default=func.now())

    ticket = relationship("Ticket",back_populates="comments")
    user = relationship("User")