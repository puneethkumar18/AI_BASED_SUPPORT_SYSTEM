from app.core.celery_app import celery
import asyncio

from app.services.email_services import EmailServices

@celery.task
def send_ticket_created_email(
    recipient: str,
    subject: str,
    body: str
):
    
    asyncio.run(EmailServices.send_email(recipient,subject,body))

    return {
        "status": "success",
        "recipient": recipient,
        "subject": subject,
        "message": "Email sent successfully"
    }
    
