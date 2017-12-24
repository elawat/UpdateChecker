from datetime import datetime, timedelta
from UpdateChecker import UpdateChecker
from Parameters import Parameters
from EmailSender import sendgmail, Email
import json



def Main():
    config_file = 'configs.json'
    params = Parameters
    epoch = datetime.utcfromtimestamp(0)
    email_details = Email
    configs = json.loads(open(config_file).read())
    days_diff = int(configs['days'])
    params.date_when_update_expired = (datetime.today() - timedelta(days=days_diff) - epoch).total_seconds()
    params.folder_path = configs['folderPath']
    params.file_name_pattern = configs['pattern']

    checker = UpdateChecker(params)
    files_not_updated = ['{}, {}'.format(file.name, file.last_modified_date)
                         for file in checker.GetNotUpdatedFiles()]

    if files_not_updated:
        email_details.senderpassword = configs['password']
        email_details.senderaddress = configs['address']
        email_details.recipientaddress = configs['recipient'].split(',')
        email_details.body = '\n'.join(files_not_updated)
        email_details.subject = 'ADS not updated'
        sendgmail(email_details)


Main()


