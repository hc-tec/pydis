
from Database.interfaces import IPersistence


class PERS_STATUS:
    NO_WRITE = 1 << 0
    WRITING = 1 << 1
    WRITED = 1 << 2
    ERROR = 1 << 3
    RE_WRITE = 1 << 4


class BasePersistence(IPersistence):

    def __init__(self, save_file_path):
        self.save_file_path = save_file_path

    def create_temp_file(self):
        pass

    def remove_temp_file(self):
        pass

