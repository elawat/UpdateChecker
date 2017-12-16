class FileAttributes:
    full_path = None
    name = None
    last_modified_date = None

    def __repr__(self):
        return "FileAttributes object: full_path: {}, name: {}, last_modified_name: {} \n".format(self.full_path,
                                                                        self.name,
                                                                        self.last_modified_date)
