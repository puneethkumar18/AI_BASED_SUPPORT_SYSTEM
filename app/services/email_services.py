from fastapi_mail import FastMail,MessageSchema,MessageType
from app.core.mail import mail_config

class EmailServices:

    @staticmethod
    async def send_mail(
        recipient: str,
        subject: str,
        body: str):

        message = MessageSchema(
            subject=subject,
            body=body,
            recipients=[recipient],
            subtype=MessageType.html
        )

        fm = FastMail(mail_config)

        await fm.send_message(message=message)
        
    