
import time
from Connection import Connection
from Protocol import RESProtocol
from Database import Database
from Command import CommandHandler
from Server import server

class Client:

    def __init__(self, client_id: int, db: Database, conn: Connection):

        self.id = client_id
        self.conn = conn
        self.db = db

        self.query_buffer = ''
        self.query_cursor = 0

        self.current_command = None
        self.create_time = time.time() * 1000
        self.last_interaction = None
        self.authenticated = True

        self.pubsub_channels = {}
        self.pubsub_patterns = []

        self.reply_buffer = []

    def is_command_input_end(self):
        print(self.query_buffer)
        return self.query_buffer.endswith('\n')

    def read_from_client(self):
        raw_read_data = self.conn.handle_read()
        self.query_buffer += raw_read_data
        if self.is_command_input_end():
            self.query_cursor += len(self.query_buffer)
            read_data = RESProtocol(self.query_buffer).parse()
            self.query_buffer = ''
            self.query_cursor = 0
            self.handle_command(read_data)
            self.conn.enable_write()

    def write_to_client(self):
        if self.reply_buffer:
            data = self.reply_buffer.pop()
            self.conn.handle_write(data)

    def append_reply(self, reply):
        self.reply_buffer.append(reply)

    def handle_command(self, cmd_data):
        handler = CommandHandler(self, cmd_data)
        handler.handle()

    def switch_database(self, db_index):
        self.db = server.get_database(db_index)
