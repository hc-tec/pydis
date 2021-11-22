

from collections import deque

from Connection.interfaces import IConnection


class Writer():

    def __init__(self):

        self._reply_buffer = deque()

    def write_to_client(self, conn: IConnection) -> int:
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

