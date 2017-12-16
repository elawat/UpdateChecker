import os
import re
from FileAttributes import FileAttributes

class FileDirScanner:

    def __init__(self, dir_path):
        self.dir_path = dir_path
        self.files_list = []


    def GetFiles(self,file_name_pattern):
        files = []

        for filename in os.listdir(self.dir_path):
            search_result =  re.search(file_name_pattern, filename)
            if search_result:
                file = FileAttributes()
                file.full_path = os.path.join(self.dir_path, filename)
                file.name = filename
                file.last_modified_date = os.path.getmtime(file.full_path)
                files.append(file)
        self.files_list = files

    def GetFilesModifiedBefore(self, before_date):
        files_modified_before = []
        for file in self.files_list:
            if file.last_modified_date < before_date:
                files_modified_before.append(file)

        return files_modified_before


