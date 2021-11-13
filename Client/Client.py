
import time
from Connection import Connection


class ReClient:

    def __init__(self, client_id: int, conn: Connection):

        self.id = client_id
        self.conn = conn
        self.db = None
        self.query_buffer = []
        self.current_command = None
        self.create_time = time.time() * 1000
        self.last_interaction = None
        self.authenticated = True

        self.pubsub_channels = {}
        self.pubsub_patterns = []

        self.__reply = ['connect']

    def read_from_client(self):
        self.query_buffer.append(self.conn.handle_read())

    def write_to_client(self):
        if self.__reply:
            data = self.__reply.pop()
            self.conn.handle_write(data)
