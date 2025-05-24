import smtplib
from twilio.rest import Client

def send_alerts(email, phone, username, is_fraud):
    subject = "ALERT: Insta Account Analysis"
    if is_fraud:
        body = f"The account @{username} appears to be fraudulent."
    else:
        body = f"The account @{username} appears safe and trustworthy."

    send_email(email, subject, body)
    send_sms(phone, body)

def send_email(to_email, subject, body):
    sender_email = "muttuh028@gmail.com"
    sender_password = "kwkmdnfivxgtgdzg"

    message = f"Subject: {subject}\n\n{body}"

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, message)

def send_sms(phone, message):
    #account_sid = 'ur SID' 
    #auth_token = ' ur Token'
    client = Client(account_sid, auth_token)

    client.messages.create(
        body=message,
        from_='+15183148296',
        to=phone
    )
