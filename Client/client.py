
import time
from Connection import Connection
from Protocol import RESProtocol
from Database import Database
from Command import CommandHandler


class Client:

    def __init__(self, client_id: int, db: Database, conn: Connection):

        self.id = client_id
        self.conn = conn
        self.db = db

        self.query_buffer = []
        self.current_command = None
        self.create_time = time.time() * 1000
        self.last_interaction = None
        self.authenticated = True

        self.pubsub_channels = {}
        self.pubsub_patterns = []

        self.reply_buffer = []

    def read_from_client(self):
        raw_read_data = self.conn.handle_read()
        read_data = RESProtocol(raw_read_data).parse()
        self.query_buffer.append(read_data)
        self.handle_command()

    def write_to_client(self):
        if self.reply_buffer:
            data = self.reply_buffer.pop()
            self.conn.handle_write(data)

    def append_reply(self, reply):
        self.reply_buffer.append(reply)

    def handle_command(self):
        handler = CommandHandler(self)
        handler.handle()
