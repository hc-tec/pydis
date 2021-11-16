
from threading import Thread

from Database.persistence.base import BasePersistence, PERS_STATUS
from Generic.json import json_dumps


class RDB(BasePersistence):

    def __init__(self, save_file_path):
        super().__init__(save_file_path)

    def save(self, server):
        # write RDB file in thread
        write_thread = RDBWriteThread(self, server)
        write_thread.start()


class RDBWriteThread(Thread):

    def __init__(self, rdb: RDB, server):
        super().__init__()
        self.rdb = rdb
        self.server = server

    def run(self) -> None:
        self.server.pers_status = PERS_STATUS.WRITING
        databases = self.server.get_databases()
        data = json_dumps(databases)
        with open(self.rdb.save_file_path, 'w') as file:
            file.write(data)
        self.server.pers_status = PERS_STATUS.WRITED
