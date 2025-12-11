import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
from app.config import settings

class EmailService:
    def init(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = settings.SMTP_EMAIL
        self.sender_password = settings.SMTP_PASSWORD
    
    async def send_verification_email(self, user_email: str, token: str):
        subject = "Verify your email"
        body = f"""
        Please verify your email by clicking the link below:
        http://localhost:8000/api/v1/auth/verify-email?token={token}
        """
        
        await self.send_email(user_email, subject, body)
    
    async def send_email(self, recipient: str, subject: str, body: str):
        message = MimeMultipart()
        message["From"] = self.sender_email
        message["To"] = recipient
        message["Subject"] = subject
        
        message.attach(MimeText(body, "plain"))
        
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.send_message(message)
            server.quit()
        except Exception as e:
            print(f"Failed to send email: {e}")

email_service = EmailService()