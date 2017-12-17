from datetime import datetime, timedelta
from UpdateChecker import UpdateChecker
from Parameters import Parameters
from EmailSender import sendgmail, Email
import json



def Main():
    gmailfile = r'C:\Users\elawa\PycharmProjects\UpdateFilesChecker\gmail.json'
    details = Parameters
    epoch = datetime.utcfromtimestamp(0)
    details.date_when_update_expired = (datetime.today() + timedelta(days=1) - epoch).total_seconds()
    details.folder_path = r'C:\Users\elawa\Desktop\test'
    details.file_name_pattern = '[aA-zZ]{2}ADS.xlsx'

    checker = UpdateChecker(details)
    files_not_updated = ['{}, {}'.format(file.name, file.last_modified_date)
                         for file in checker.GetNotUpdatedFiles()]

    if files_not_updated:
        emaildetails = Email
        credentials = json.loads(open(gmailfile).read())
        emaildetails.senderpassword = credentials['password']
        emaildetails.senderaddress = credentials['address']
        emaildetails.recipientaddress = credentials['recipient'].split(',')
        emaildetails.body = '\n'.join(files_not_updated)
        emaildetails.subject = 'ADS not updated'
        sendgmail(emaildetails)




Main()



