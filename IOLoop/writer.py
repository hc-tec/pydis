

from collections import deque

from Connection.interfaces import IConnection
from IOLoop.interfaces import IWriter


class Writer(IWriter):

    def __init__(self):

        self._reply_buffer = deque()

    def write_to_client(self, conn: IConnection) -> int:
        # if not len(self._reply_buffer):
        #     return 1
        # data = self._reply_buffer.pop()
        # if not conn.ready_to_write(data):
        #     return 0
        # if not len(self._reply_buffer):
        #     conn.enable_read()
        # return 1
        while len(self._reply_buffer):
            data = self._reply_buffer.pop()
            if not conn.ready_to_write(data):
                return 0
            conn.enable_read()
        return 1

    def append_reply(self, reply):
        self._reply_buffer.appendleft(reply)

    def is_reply_empty(self):
        return len(self._reply_buffer) == 0

