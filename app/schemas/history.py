from pydantic import BaseModel,ConfigDict
from typing import Optional
from datetime import datetime

class HistoryResponse(BaseModel):
    id:int
    action:str
    ticket_id:int
    performed_by:int
    old_value:Optional[str]=None
    new_value:Optional[str]=None
    created_at:datetime

    model_config = ConfigDict(
        from_attributes= True
    )
