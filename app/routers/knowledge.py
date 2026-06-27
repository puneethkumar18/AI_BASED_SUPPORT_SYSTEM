from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.services.knowledge_service import KnowledgeServices
from app.schemas.knowledge import (KnowledgeResponse,KnowledgeCreate,KnowledgeUpdate)
from typing import List
from app.models.user import User
from app.auth.dependencies import require_roles
from app.core.enums import RoleEnum

router = APIRouter(prefix="/knowledge",tags=["Knowledge"])


@router.post("",response_model=KnowledgeResponse)
def create_knowledge(
    knowledge_data:KnowledgeCreate,
    db:Session=Depends(get_db),
    current_user:User=Depends(require_roles(RoleEnum.ADMIN,RoleEnum.CUSTOMER))):

    article = KnowledgeServices.create_knowledge(db,knowledge_data)
    return article

@router.get("",response_model=List[KnowledgeResponse])
def get_knowledge(db:Session=Depends(get_db)):
    articles = KnowledgeServices.get_all_knowledge(db)
    return articles


@router.get("/{knowledge_id}",response_model=KnowledgeResponse)
def get_knowledge_byId(knowledge_id:int,db:Session=Depends(get_db)):
    article = KnowledgeServices.get_by_id(db,knowledge_id)
    if article is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Knowledge for this id is not exists"
        )
    return article


@router.patch("/{knowledge_id}",response_model=KnowledgeResponse)
def update_knowledge(
    knowledge_id:int,
    knowledge_data:KnowledgeUpdate,
    db:Session=Depends(get_db),
    current_user:User = Depends(require_roles(RoleEnum.ADMIN,RoleEnum.SUPPORT_AGENT))):
    article = KnowledgeServices.get_by_id(db,knowledge_id)
    if article is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Knowledge Not Found"
        )
    return KnowledgeServices.update_knowledge(db,article,knowledge_data)

@router.delete("/{knowledge_id}")
def delete_knowledge(
    knowledge_id:int,
    db:Session=Depends(get_db),
    current_user:User=Depends(require_roles(RoleEnum.ADMIN))):
    article = KnowledgeServices.get_by_id(db,knowledge_id)
    if article is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Knowledge Not Found"
        )
    KnowledgeServices.delete(db,article)
    return {
        "message":"Knowledge has been Deleted from database!"
    }