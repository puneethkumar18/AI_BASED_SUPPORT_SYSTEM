from app.database.database import Base
from sqlalchemy import Column,Integer,String,DateTime,Text
from sqlalchemy.sql import func

class KnowledgeBase(Base):
    __tablename__ = "knowledge_base"

    id=Column(Integer,primary_key=True,index=True)
    title = Column(String,nullable=False)
    content = Column(Text,nullable=False)
    category = Column(String,nullable=False)
    created_at = Column(DateTime(timezone=True),server_default=func.now())
    updated_at = Column(DateTime(timezone=True),server_default=func.now(),server_onupdate=func.now())
