from pydantic import BaseModel
from datetime import datetime
from pydantic import ConfigDict


class AttachmentResponse(BaseModel):
    id:int
    file_name:str
    stored_file_name:str
    file_size:int
    content_type: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )