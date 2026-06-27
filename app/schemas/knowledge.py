from pydantic import BaseModel,ConfigDict
from typing import Optional
from datetime import datetime

class KnowledgeCreate(BaseModel):
    title:str
    content:str
    category:str


class KnowledgeUpdate(BaseModel):
    title:Optional[str]=None
    content:Optional[str]=None
    category:Optional[str]=None


class KnowledgeResponse(BaseModel):
    id: int
    title:str
    content:str
    category:str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)