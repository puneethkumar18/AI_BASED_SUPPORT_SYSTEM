from sqlalchemy.orm import Session

from app.models.knowledge_base import KnowledgeBase
from app.schemas.knowledge import (KnowledgeCreate,KnowledgeResponse,KnowledgeUpdate)

class KnowledgeServices:
    @staticmethod
    def create_knowledge(db:Session,data:KnowledgeCreate):
        article = KnowledgeBase(
            **data.model_dump()
        )

        db.add(article)
        db.commit()
        db.refresh(article)
        return article
    
    @staticmethod
    def get_all_knowledge(db:Session):
        articles = db.query(KnowledgeBase).all()
        return articles
    
    @staticmethod
    def get_by_id(db:Session,article_id: int):
        article = db.query(KnowledgeBase).filter(KnowledgeBase.id == article_id).first()
        return article
    
    @staticmethod
    def update_knowledge(db:Session,article:KnowledgeBase,data: KnowledgeUpdate):
        update_data = data.model_dump(
            exclude_unset=True
        )

        for key,value in update_data.items():
            setattr(article,key,value)

        db.commit()
        db.refresh(article)
        return article
    
    @staticmethod
    def delete(db:Session,article: KnowledgeBase):
        db.delete(article)
        db.commit()
        