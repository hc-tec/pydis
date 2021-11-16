
from threading import Thread

from Database.persistence.base import BasePersistence


class AOF_FSYNC_TYPE:
    ALWAYS = 0
    EVERY_SECOND = 1 << 0
    NO = 1 << 1


class AOF(BasePersistence):

    def save(self, server):
        write_thread = AOFWriteThread(server, self)
        write_thread.start()


class AOFWriteThread(Thread):

    def __init__(self, server, aof: AOF):
        super().__init__()
        self.server = server
        self.aof = aof

    def run(self) -> None:
        with open(self.aof.save_file_path, 'a+') as file:
            for buf in self.server.aof_buf:
                file.write(f'{buf}\n')
        self.server.aof_buf = []

