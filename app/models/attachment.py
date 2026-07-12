from sqlalchemy import Column,Integer,ForeignKey,String,DateTime
from sqlalchemy.sql import func
from app.database.database import Base
from sqlalchemy.orm import relationship


class Attachment(Base):
    __tablename__ = "attachments"


    id = Column(Integer,primary_key=True,index=True)
    ticket_id = Column(Integer,ForeignKey("tickets.id"),nullable=False)
    uploaded_by = Column(Integer,ForeignKey("users.id"),nullable=False)
    file_name  = Column(String, nullable=False)
    stored_file_name  = Column(String, nullable=False)
    file_path  = Column(String, nullable=False)
    file_size = Column(Integer,nullable=False)
    content_type = Column(String,nullable=False)
    created_at = Column(DateTime(timezone=True),server_default=func.now())

    ticket = relationship("Ticket",back_populates="attachments")
    user = relationship("User")
    