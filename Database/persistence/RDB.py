
from threading import Thread

from Database.database import Database
from Database.persistence.base import BasePersistence, PERS_STATUS
from Generic.json import json_dumps, json_loads


RDB_FILE_READ_MAX = 1024


class RDB(BasePersistence):

    def __init__(self, save_file_path):
        super().__init__(save_file_path)

    def save(self, server):
        # write RDB file in thread
        write_thread = RDBWriteThread(self, server)
        write_thread.start()

    def load(self, server):
        try:
            with open(self.save_file_path, 'r') as file:
                file_data = file.readlines()
                data = ''.join(file_data)
            self.load_from_data(server, data)
        except FileNotFoundError:
            pass

    def load_from_data(self, server, data):
        data = json_loads(data)
        databases = server.get_databases()
        for index, database_dict in enumerate(data):
            database: Database = databases[index]
            database.initial_with_dict(database_dict)


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
