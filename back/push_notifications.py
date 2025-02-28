from itsdangerous import URLSafeSerializer
import smtplib
import json
from email.mime.text import MIMEText


ngrok_ = "https://ewsenku.vercel.app"
SECRET_KEY = "SfS5JXWwmn"
serialiser = URLSafeSerializer(SECRET_KEY)

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
SMTP_EMAIL = "econnecttech5@gmail.com"
SMTP_PASSWORD = "snux ednn oexs bftw"


def send_verification_email(email, name):
    token = serialiser.dumps(email, salt="email-verification")
    verification_link = f"{ngrok_}/centers/verify/{token}"  # ✅ Make sure URL is correct
    msg = MIMEText(f"Hi {name},\n\nClick this link to verify your login: {verification_link}")
    msg["Subject"] = "Recycler Login Verification"
    msg["From"] = SMTP_EMAIL
    msg["To"] = email
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.sendmail(SMTP_EMAIL, email, msg.as_string())

def send_status_email(email, itemName, status):
    msg = MIMEText(f"Your item '{itemName}' status has been updated to: {status}.")
    msg["Subject"] = "E-Waste Recycling Status Update!"
    msg["From"] = SMTP_EMAIL
    msg["To"] = email
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.sendmail(SMTP_EMAIL, email, msg.as_string())


def send_newItem_email(center_email, itemName, itemCount):
    msg = MIMEText(f"({itemCount}){itemName} has been listed!")
    msg["Subject"] = "E-Waste Recycling Status Update!"
    msg["From"] = SMTP_EMAIL
    msg["To"] = center_email
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.sendmail(SMTP_EMAIL, center_email, msg.as_string())