from datetime import datetime, timedelta
import json
from FileDirScanner import FileDirScanner
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def sendgmail(email_details):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(email_details['senderaddress'], email_details['senderpassword'])
    msg = MIMEMultipart()
    message = email_details['body']

    msg['From'] = email_details['senderaddress']
    recipients = ', '.join(email_details['recipientaddress'])
    msg['To'] = recipients
    msg['Subject'] = email_details['subject']
    msg.attach(MIMEText(message, 'plain'))
    server.send_message(msg)


def get_not_updated_files(params):
    scanner = FileDirScanner(params['folder_path'])
    scanner.get_files(params['name_pattern'])
    return scanner.get_files_modified_before(params['date_when_update_expired'])


def check_ads_updates():
    config_file = 'configs.json'
    configs = json.loads(open(config_file).read())
    epoch = datetime.utcfromtimestamp(0)
    days_diff = int(configs['days'])
    params = {'folder_path': configs['folderPath'], 'name_pattern': configs['pattern'],
              'date_when_update_expired': (datetime.today() - timedelta(days=days_diff) - epoch).total_seconds()}

    files_not_updated = ['{}, {}'.format(file.name, file.last_modified_date)
                         for file in get_not_updated_files(params)]

    if files_not_updated:
        email_details = {'senderpassword': configs['password'],
                         'senderaddress': configs['address'],
                         'recipientaddress': configs['recipient'].split(','),
                         'body': '\n'.join(files_not_updated),
                         'subject': 'ADS not updated'}
        sendgmail(email_details)


if __name__ == "__main__":
    check_ads_updates()
