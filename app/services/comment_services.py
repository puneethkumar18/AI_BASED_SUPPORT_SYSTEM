from sqlalchemy.orm import Session
from app.schemas.comment import CommentCreate
from app.models.comment import Comment
from app.models.ticket import Ticket
from app.models.user import User
from app.services.email_services import EmailServices
from fastapi import BackgroundTasks
from app.exceptions.custom_exception import *

class CommentServices:

    @staticmethod
    def add_comment(
        db:Session,
        ticket:Ticket,
        current_user:User,
        comment_data:CommentCreate,
        background_tasks:BackgroundTasks,
        ):
        comment = Comment(
            message = comment_data.message,
            ticket_id=ticket.id,
            user_id = current_user.id
        )
        created_by = db.query(User).filter(User.id == ticket.created_by).first()
        db.add(comment)
        db.commit()
        db.refresh(comment)

        background_tasks.add_task(
           EmailServices.send_email,
           recipient=created_by.email,
           subject="New Comment on Your Ticket",
           body=comment.message
        )

        return comment
    
    @staticmethod
    def get_comments(db:Session,ticket_id:int):
        comments = (db.query(Comment)
                    .filter(Comment.ticket_id == ticket_id)
                    .order_by(Comment.created_at.desc())
                    .all())

        if len(comments) == 0:
            raise ValueErrorException("No Comments")
        return comments
    

    @staticmethod
    def delete_comment(db:Session,comment_id:int):
        comment = db.query(Comment).filter(Comment.id == comment_id).first()
        if comment is None:
            raise CommentNotFoundException
        db.delete(comment)
        db.commit()
        return {
            "messgae":"Comment has been deleted"
        }