
from collections import deque
from typing import Optional

from Connection import Connection
from Protocol import RESProtocol
from Database import Database
from Command.base import BaseCommand, CommandType
from Command.handler import CommandHandler
from Generic.time import get_cur_time
from Replication.base import REPL_SLAVE_STATE


class Client:

    def __init__(self, server, client_id: int, db: Database, conn: Connection):
        self.server = server
        self.id = client_id
        self.conn = conn
        self.db = db

        self.query_buffer = ''
        self.query_cursor = 0

        self.current_command: Optional[BaseCommand] = None
        self.create_time = get_cur_time()
        self.last_interaction = None
        self.authenticated = True

        # Replication
        self.repl_state = REPL_SLAVE_STATE.NONE
        self.repl_ack_time = None

        # transaction
        self.ms_state = None

        self.watch_keys = []
        self.pubsub_channels = {}
        self.pubsub_patterns = []

        self.reply_buffer = []

    def is_command_input_end(self):
        print(self.query_buffer)
        return self.query_buffer.endswith('\n')

    def read_from_conn(self):
        raw_read_data = self.conn.handle_read()
        self.query_buffer += raw_read_data
        if self.is_command_input_end():
            self.query_cursor += len(self.query_buffer)
            read_data = RESProtocol(self.query_buffer).parse()
            self.query_buffer = ''
            self.query_cursor = 0
            return read_data
        return None

    def read_from_client(self):
        read_data = self.read_from_conn()
        if read_data is None: return
        self.slave_check(read_data)
        self.handle_command(read_data)
        self.conn.enable_write()

    def write_to_client(self):
        if self.reply_buffer:
            data = self.reply_buffer.pop()
            self.conn.handle_write(data)
            self.conn.enable_read()

    def append_reply(self, reply):
        self.reply_buffer.append(reply)

    def handle_command(self, cmd_data):
        handler = CommandHandler(self, cmd_data)
        handler.handle()

    # def switch_database(self, db_index):
    #     self.db = server.get_database(db_index)
    #
    def get_server(self):
        return self.server

    def set_current_command(self, command: BaseCommand):
        self.current_command = command
        if command and command.cmd_type & CommandType.CMD_WRITE:
            self.server.write_cmd_increment()
            self.server.aof_buf.append(command.raw_cmd)

    def slave_check(self, read_data: str):
        if read_data.startswith('REPLCONF listening-port'.lower()):
            self.repl_state = REPL_SLAVE_STATE.RECEIVE_PORT
            self.server.repl_slaves.append(self)
        elif read_data.startswith('REPLCONF ip-address'.lower()):
            self.repl_state = REPL_SLAVE_STATE.RECEIVE_IP
        elif read_data.startswith('SYNC'.lower()):
            self.repl_state = REPL_SLAVE_STATE.RECEIVE_PSYNC
        elif read_data.startswith('(ok)'.lower()):
            if self.repl_state == REPL_SLAVE_STATE.RECEIVE_PSYNC:
                self.repl_state = REPL_SLAVE_STATE.TRANSFER
            elif self.repl_state == REPL_SLAVE_STATE.TRANSFER:
                self.repl_state = REPL_SLAVE_STATE.CONNECTED
