from sqlalchemy.orm import Session
from app.schemas.comment import CommentCreate
from app.models.comment import Comment
from app.models.ticket import Ticket
from app.models.user import User
from app.services.email_services import EmailServices

class CommentServices:

    @staticmethod
    async def add_comment(db:Session,ticket:Ticket,current_user:User,comment_data:CommentCreate):
        comment = Comment(
            message = comment_data.message,
            ticket_id=ticket.id,
            user_id = current_user.id
        )

        db.add(comment)
        db.commit()
        db.refresh(comment)

        await EmailServices.send_mail(
            recipient="puneethkumar96@gmail.com",
            subject="New Comment on Your Ticket",
            body=comment.message
        )

        return comment
    
    @staticmethod
    def get_comments(db:Session,ticket_id:int):
        comments = (db.query(Comment)
                    .filter(Comment.ticket_id == ticket_id)
                    .order_by(Comment.created_at.asc())
                    .all())
        return comments