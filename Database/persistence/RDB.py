
from threading import Thread

from typing import List
from Timer.timer import SaveParam
from Database.interfaces import IDatabase, IDatabaseManager
from Database.persistence.base import PERS_STATUS
from Database.persistence.interfaces import IPersistenceManager, IRDBManager, IRDB
from Generic.json import json_dumps, json_loads
from Conf import app
from Generic.time import get_cur_time


SETTINGS = app.get_settings()


RDB_FILE_READ_MAX = 1024


class RDB(IRDB):

    def save(self, db_manager: IDatabaseManager, persist_manager: IPersistenceManager):
        # write RDB file in thread
        write_thread = RDBWriteThread(
            rdb=self,
            persist_manager=persist_manager,
            db_manager=db_manager
        )
        write_thread.start()

    def load(self, db_manager: IDatabaseManager):
        try:
            with open(self.get_save_file_path(), 'r') as file:
                file_data = file.readlines()
                data = ''.join(file_data)
            self.load_from_data(db_manager, data)
        except FileNotFoundError:
            pass

    def load_from_data(self, db_manager: IDatabaseManager, data):
        data = json_loads(data)
        databases = db_manager.get_databases()
        for index, database_dict in enumerate(data):
            database: IDatabase = databases[index]
            database.initial_with_dict(database_dict)


class RDBWriteThread(Thread):

    def __init__(self, rdb: IRDB, persist_manager: IPersistenceManager, db_manager: IDatabaseManager):
        super().__init__()
        self.rdb = rdb
        self.db_manager = db_manager
        self.persist_manager = persist_manager

    def run(self) -> None:
        self.persist_manager.set_pers_status(PERS_STATUS.WRITING)
        databases = self.db_manager.get_databases()
        data = json_dumps(databases)
        with open(self.rdb.get_save_file_path(), 'w') as file:
            file.write(data)
        self.persist_manager.set_pers_status(PERS_STATUS.WRITED)


class RDBManager(IRDBManager):

    def __init__(self):
        # RDB persistence
        self._enable = True
        self._save_params: List[SaveParam] = [
            SaveParam(900, 1),
            SaveParam(300, 10),
            SaveParam(10, 1)
        ]
        self._dirty = 0
        self._dirty_before_bgsave = get_cur_time()
        self._filename = SETTINGS.RDB_FILE
        self._compression = False
        self._checksum = 0

        self._last_save = None
        self._save_time_start = 0

    def get_file_path(self):
        return self._filename

    def get_dirty(self):
        return self._dirty

    def incr_dirty(self):
        self._dirty += 1

    def get_dirty_before_bgsave(self):
        return self._dirty_before_bgsave

    def get_save_params(self):
        return self._save_params

    def reset(self):
        self._dirty = 0
        self._dirty_before_bgsave = get_cur_time()

    def start(self, db_manager: IDatabaseManager, persist_manager: IPersistenceManager):
        rdb = RDB(self._filename)
        rdb.save(persist_manager=persist_manager, db_manager=db_manager)
        self.reset()

    def load_file(self, db_manager: IDatabaseManager):
        rdb = RDB(SETTINGS.RDB_FILE)
        rdb.load(db_manager)

    def load_from_master(self, db_manager: IDatabaseManager, data):
        rdb = RDB(None)
        rdb.load_from_data(db_manager, data)

    def is_enable(self):
        return self._enable

    def enable(self):
        self._enable = True

    def disabled(self):
        self._enable = False


