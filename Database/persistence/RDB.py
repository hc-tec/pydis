

from Database.persistence.base import BasePersistence


class RDB(BasePersistence):

    def __init__(self, save_file_path):
        super().__init__(save_file_path)

    def save(self, server):
        print('save')
        pass




