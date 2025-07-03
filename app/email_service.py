import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from decouple import config
import logging

# Email configuration
SMTP_SERVER = config("SMTP_SERVER", default="smtp.gmail.com")
SMTP_PORT = int(config("SMTP_PORT", default=587))
EMAIL_USERNAME = config("EMAIL_USERNAME", default="")
EMAIL_PASSWORD = config("EMAIL_PASSWORD", default="")
EMAIL_FROM = config("EMAIL_FROM", default="")

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.smtp_server = SMTP_SERVER
        self.smtp_port = SMTP_PORT
        self.username = EMAIL_USERNAME
        self.password = EMAIL_PASSWORD
        self.from_email = EMAIL_FROM
    
    def send_email(self, to_email: str, subject: str, body: str, is_html: bool = False) -> bool:
        """Send email using SMTP"""
        if not all([self.username, self.password, self.from_email]):
            logger.warning("Email configuration not complete. Skipping email send.")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add body
            msg.attach(MIMEText(body, 'html' if is_html else 'plain'))
            
            # Connect to server and send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.username, self.password)
            text = msg.as_string()
            server.sendmail(self.from_email, to_email, text)
            server.quit()
            
            logger.info(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False
    
    def send_verification_email(self, to_email: str, verification_url: str) -> bool:
        """Send email verification email"""
        subject = "Verify Your Email Address"
        body = f"""
        <html>
        <body>
            <h2>Email Verification</h2>
            <p>Thank you for signing up! Please click the link below to verify your email address:</p>
            <p><a href="{verification_url}">Verify Email Address</a></p>
            <p>If you didn't create an account, please ignore this email.</p>
            <p>This link will expire in 1 hour.</p>
        </body>
        </html>
        """
        return self.send_email(to_email, subject, body, is_html=True)

# Global email service instance
email_service = EmailService()
