
import smtplib
from email.mime.text import MIMEText
from django.conf import settings

def send(to_addr, from_addr, title, message):

    msg = MIMEText(message, "html")
    msg["Subject"] = title
    msg["To"] = to_addr
    msg["From"] = from_addr

    server = smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
    server.send_message(msg)
    server.quit()