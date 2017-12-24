# import the smtplib module. It should be included in Python by default
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Email:
    sender_address = None
    sender_password = None
    body = 'no body text'
    recipient_address = []
    subject = 'no subject'


def sendgmail(email_details):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(email_details.senderaddress, email_details.senderpassword)
    msg = MIMEMultipart()
    message = email_details.body

    msg['From']=email_details.senderaddress
    recipients = ', '.join(email_details.recipientaddress)
    msg['To']=recipients
    msg['Subject']=email_details.subject
    msg.attach(MIMEText(message, 'plain'))
    server.send_message(msg)