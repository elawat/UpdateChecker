from FileDirScanner import FileDirScanner
from Parameters import Parameters


class UpdateChecker:

    def __init__(self, details: Parameters ):
        self.details = details

    def GetNotUpdatedFiles(self):
        scanner = FileDirScanner(self.details.folder_path)
        scanner.GetFiles(self.details.file_name_pattern)
        return scanner.GetFilesModifiedBefore(self.details.date_when_update_expired)






