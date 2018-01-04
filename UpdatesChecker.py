import json
import smtplib
import re
import os
import win32com.client
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import strftime, localtime

THIS_FILE = os.path.abspath(__file__)
PROJECT_DIR = os.path.dirname(THIS_FILE)


def get_files(dir_path, file_name_pattern):
    files = []

    for filename in os.listdir(dir_path):
        search_result = re.search(file_name_pattern, filename.lower())
        if search_result:
            file = {'full_path': os.path.join(dir_path, filename), 'name': filename,
                    'last_modified_date': os.path.getmtime(os.path.join(dir_path, filename))}
            files.append(file)
    return files


def get_files_modified_before(files, before_date):
    files_modified_before = []
    for file in files:
        if file['last_modified_date'] < before_date:
            files_modified_before.append(file)
    return files_modified_before


def get_not_updated_files(params):
    files = get_files(params['folder_path'], params['name_pattern'])
    return get_files_modified_before(files, params['date_when_update_expired'])


def send_cdo_msg(recipients, subject, body, sent_from):
    conf = win32com.client.Dispatch("CDO.Configuration")
    flds = conf.Fields
    flds("http://schemas.microsoft.com/cdo/configuration/smtpserver").Value = ""
    flds("http://schemas.microsoft.com/cdo/configuration/smtpserverport").Value = 25
    flds("http://schemas.microsoft.com/cdo/configuration/sendusing").Value = 2  # cdoSendUsingPort
    # Authentication and stuff
    flds('http://schemas.microsoft.com/cdo/configuration/smtpauthenticate').Value = 0  # No authentication
    # The following fields are only used if the previous authentication value is set to 1 or 2
    # flds('http://schemas.microsoft.com/cdo/configuration/smtpaccountname').Value = "user"
    # flds('http://schemas.microsoft.com/cdo/configuration/sendusername').Value = "elzbietawatroba@economist.com"
    flds('http://schemas.microsoft.com/cdo/configuration/smtpusessl').Value = False
    # flds('http://schemas.microsoft.com/cdo/configuration/sendpassword').Value = "password"
    flds.Update()
    msg = win32com.client.Dispatch("CDO.Message")
    msg.Configuration = conf
    msg.To = recipients
    msg.From = sent_from
    msg.Subject = subject
    msg.TextBody = body
    msg.Send()


def send_email(email_details):
    server = smtplib.SMTP('', 25)
    server.ehlo()
    server.starttls()
    # server.login(email_details['senderaddress'], email_details['senderpassword'])
    msg = MIMEMultipart()
    message = email_details['body']

    msg['From'] = email_details['sender']
    recipients = ', '.join(email_details['recipient_address'])
    msg['To'] = recipients
    msg['Subject'] = email_details['subject']
    msg.attach(MIMEText(message, 'plain'))
    server.send_message(msg)


def check_updates():
    config_file = os.path.join(PROJECT_DIR, 'configs.json')
    with open(config_file) as fh:
        configs = json.load(fh)
    folders_to_check = configs['folderPath'].split(',')
    for folder in folders_to_check:
        epoch = datetime.utcfromtimestamp(0)
        days_diff = configs['days']
        params = {'folder_path': folder, 'name_pattern': configs['pattern'],
                  'date_when_update_expired': (datetime.today() - timedelta(days=days_diff) - epoch).total_seconds()}

        files_not_updated = [
            '{}, {}'.format(file['name'], strftime("%a, %d %b %Y %H:%M:%S", localtime(file['last_modified_date'])))
            for file in get_not_updated_files(params)]

        if files_not_updated:
            send_cdo_msg(configs['recipient'], configs['subject'] + folder, '\n'.join(files_not_updated),
                         configs['sender'])


if __name__ == "__main__":
    check_updates()
