from datetime import datetime


class FileModel:
    def __init__(self, file: bytes, file_name: str, mimetype: str = "image/jpg"):
        self.file = file
        self.file_name = file_name
        self.mimetype = mimetype
        self.created_at = datetime.now()

    def to_dict(self):
        return self.__dict__
