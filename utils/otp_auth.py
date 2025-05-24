import random
import smtplib
import os
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

otp_store = {}

def generate_otp():
    return str(random.randint(100000, 999999))

# Email OTP
def send_email_otp(email):
    if not email:
        raise ValueError("Email address is required.")

    otp = generate_otp()
    otp_store[email] = otp

    sender_email = os.getenv("EMAIL_ADDRESS")
    sender_password = os.getenv("EMAIL_PASSWORD")

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            message = f"Subject: Insta Fraud OTP\n\nYour OTP is: {otp}"
            server.sendmail(sender_email, email, message)
    except Exception as e:
        raise RuntimeError(f"Failed to send email OTP: {e}")

# SMS OTP
def send_sms_otp(phone):
    if not phone:
        raise ValueError("Phone number is required.")

    if not phone.startswith('+'):
        raise ValueError("Phone number must be in E.164 format (start with '+').")

    otp = generate_otp()
    otp_store[phone] = otp

    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    twilio_number = os.getenv('TWILIO_PHONE_NUMBER')

    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=f"Your Insta Fraud OTP is: {otp}",
            from_=twilio_number,
            to=phone
        )
        return message.sid
    except Exception as e:
        raise RuntimeError(f"Failed to send SMS OTP: {e}")

# OTP verification
def verify_otp(identifier, otp):
    return otp_store.get(identifier) == otp
