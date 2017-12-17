# import the smtplib module. It should be included in Python by default
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Email:
    senderaddress = None
    senderpassword = None
    body = 'no body text'
    recipientaddress = []
    subject = 'no subject'


def sendgmail(emaildetails):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(emaildetails.senderaddress, emaildetails.senderpassword)
    msg = MIMEMultipart()
    message = emaildetails.body

    msg['From']=emaildetails.senderaddress
    recipients = ', '.join(emaildetails.recipientaddress)
    msg['To']=recipients
    msg['Subject']=emaildetails.subject
    msg.attach(MIMEText(message, 'plain'))
    server.send_message(msg)