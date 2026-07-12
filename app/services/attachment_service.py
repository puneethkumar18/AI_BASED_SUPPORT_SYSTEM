from app.services.file_services import FileServices
from sqlalchemy.orm import Session
from app.models.ticket import Ticket
from app.models.user import User
from app.models.attachment import Attachment

class AttachmentService:
    @staticmethod
    def upload_file(db:Session,ticket:Ticket,current_user:User,file):
        saved = FileServices.save_file(file)

        attachment = Attachment(
            file_name=file.filename,
            stored_file_name = saved["stored_filename"],
            file_path = saved["file_path"],
            content_type=file.content_type,
            file_size=file.size,
            ticket_id=ticket.id,
            uploaded_by=current_user.id
        )
        db.add(attachment)
        db.commit()
        db.refresh(attachment)

        return attachment