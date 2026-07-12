from app.core.celery_app import celery

from app.services.email_services import EmailServices

@celery.task
def send_ticket_created_email(
    recipient: str,
    subject: str,
    body: str
):
    EmailServices.send_mail(recipient,subject,body)
