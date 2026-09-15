import smtplib
from email.message import EmailMessage
from config import EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER, SMTP_SERVER, SMTP_PORT

def send_email(subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
        print(f"Email sent: {subject}")
    except Exception as e:
        print(f"Failed to send email: {e}")
