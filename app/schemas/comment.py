from pydantic import BaseModel,ConfigDict
from typing import Optional
from datetime import datetime

class CommentCreate(BaseModel):
    message :str 


class CommentUpdate(BaseModel):
    id:int
    message:str

class CommentResponse(BaseModel):
    id:int
    message:str
    user_id:int
    ticket_id:int
    created_at:datetime
    model_config = ConfigDict(
        from_attributes=True
    )