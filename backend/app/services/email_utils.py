import os
from email.message import EmailMessage
import aiosmtplib
from dotenv import load_dotenv

load_dotenv()

async def send_reset_email(to_email: str, reset_link: str):
    msg = EmailMessage()
    msg["From"] = os.getenv("FROM_EMAIL")
    msg["To"] = to_email
    msg["Subject"] = "Password Reset for JobTrackerDB"
    msg.set_content(f"Click the link to reset your password: {reset_link}")

    await aiosmtplib.send(
        msg,
        hostname=os.getenv("SMTP_HOST"),
        port=int(os.getenv("SMTP_PORT")),
        username=os.getenv("SMTP_USER"),
        password=os.getenv("SMTP_PASS"),
        start_tls=True,
    ) 