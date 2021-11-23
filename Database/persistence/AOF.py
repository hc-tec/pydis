
from threading import Thread

from Database.interfaces import IDatabaseManager
from Database.persistence.interfaces import IAOFManager, IPersistenceMethod, IPersistenceManager
from Conf import app
from Generic.time import get_cur_time


SETTINGS = app.get_settings()


class AOF_FSYNC_TYPE:
    ALWAYS = 0
    EVERY_SECOND = 1 << 0
    NO = 1 << 1


class AOF(IPersistenceMethod):

    def save(self,
             aof_manager: IAOFManager,
             db_manager: IDatabaseManager,
             persist_manager: IPersistenceManager):

        write_thread = AOFWriteThread(aof_manager, self)
        write_thread.start()

    def load(self, server):
        ...


class AOFWriteThread(Thread):

    def __init__(self, aof_manager: IAOFManager, aof: IPersistenceMethod):
        super().__init__()
        self.aof_manager = aof_manager
        self.aof = aof

    def run(self) -> None:
        with open(self.aof.get_save_file_path(), 'a+') as file:
            for buf in self.aof_manager.get_buffer():
                file.write(f'{buf}\n')
        self.aof_manager.clear_buffer()


class AOFManager(IAOFManager):

    def __init__(self):
        # AOF Persistence
        self._filename = SETTINGS.AOF_FILE
        self._buffer = []
        self._enable = True
        self._fsync = AOF_FSYNC_TYPE.EVERY_SECOND
        self._rewrite_last_time = get_cur_time()

    def get_file_path(self):
        return self._filename

    def get_buffer(self):
        return self._buffer

    def append_to_buffer(self, data):
        self._buffer.append(data)

    def clear_buffer(self):
        self._buffer = []

    def get_rewrite_last_time(self):
        return self._rewrite_last_time

    def reset_rewrite_time(self):
        self._rewrite_last_time = get_cur_time()

    def start(self, db_manager: IDatabaseManager, persist_manager: IPersistenceManager):
        aof = AOF(self._filename)
        aof.save(self, db_manager, persist_manager)

    def is_enable(self):
        return self._enable

    def enable(self):
        self._enable = True

    def disabled(self):
        self._enable = False

    def reset(self):
        ...

    def load_file(self, db_manager: IDatabaseManager):
        ...
