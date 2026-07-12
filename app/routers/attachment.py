from fastapi import Depends,APIRouter,UploadFile,File,HTTPException
from app.schemas.attachment import AttachmentResponse
from app.services.attachment_service import AttachmentService
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.auth.dependencies import get_current_user
from app.services.ticket_services import TicketServices
from app.models.attachment import Attachment

from fastapi.responses import FileResponse

router  =  APIRouter(prefix="/tickets",tags=["Attachments"])

@router.post("{/ticket_id/attachments}",response_model=AttachmentResponse)
def upload_attachment(
    ticket_id:int,
    file: UploadFile = File(...),
    db:Session=Depends(get_db),
    current_user=Depends(get_current_user)):

    ticket = TicketServices.get_ticket_by_id(db,ticket_id)
    if ticket is None:
        raise HTTPException("Ticket not found.",status_code=404)
    
    return AttachmentService.upload_file(db,ticket,current_user,file)


@router.get("/attachments/{attachment_id}/download")
def download_attachment(
    attachment_id:int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
    ):

    attachment = (
        db.query(Attachment)
        .filter(Attachment.id == attachment_id)
        .first()
    )

    if attachment is None:
        raise HTTPException(
            status_code=404,
            detail="Attachment not found."
        )
    
    return FileResponse(path=attachment.file_path,filename=attachment.file_name)