import smtplib
from email.message import EmailMessage
from config import EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER, SMTP_SERVER, SMTP_PORT

def send_email(subject, body, link=None, price=None):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_SENDER
    # Handle multiple recipients separated by comma
    receivers = [r.strip() for r in EMAIL_RECEIVER.split(',')]
    msg['To'] = ", ".join(receivers)

    html_body = f"""
    <html>
    <body style="font-family: sans-serif; line-height: 1.6;">
        <h2 style="color: #2c3e50;">New Pinball Listing Found!</h2>
        <p><strong>Item:</strong> {body}</p>
        <p><strong>Price:</strong> £{price}</p>
        <p><a href="{link}" style="background-color: #3498db; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">View Listing</a></p>
    </body>
    </html>
    """
    msg.add_alternative(html_body, subtype='html')

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
        print(f"Email sent: {subject}")
    except Exception as e:
        print(f"Failed to send email: {e}")
