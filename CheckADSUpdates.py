from datetime import datetime, timedelta
from UpdateChecker import UpdateChecker
from Parameters import Parameters


def Main():
    details = Parameters
    epoch = datetime.utcfromtimestamp(0)
    details.date_when_update_expired = (datetime.today() + timedelta(days=1) - epoch).total_seconds()
    details.folder_path = r'C:\Users\elawa\Desktop\test'
    details.file_name_pattern = '[aA-zZ]{2}ADS.xlsx'

    checker = UpdateChecker(details)
    files_not_updated = checker.GetNotUpdatedFiles()

    if files_not_updated:
        for file in files_not_updated:
            print(file.name)
        print(files_not_updated)


Main()



