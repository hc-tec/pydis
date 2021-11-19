
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
        self.read_data = ''

        self.current_command: Optional[BaseCommand] = None
        self.create_time = get_cur_time()
        self.last_interaction = None
        self.authenticated = True

        # Replication
        self.repl_state = REPL_SLAVE_STATE.NONE
        self.repl_ack_time = None
        # (host, port), used in master keepalive system
        self.host_as_slave = None
        self.port_as_slave = None

        # transaction
        self.ms_state = None

        self.watch_keys = []
        self.pubsub_channels = {}
        self.pubsub_patterns = []

        self.reply_buffer = deque()

    @staticmethod
    def is_slave_connected(cls):
        return cls.repl_state == REPL_SLAVE_STATE.CONNECTED

    def is_command_input_end(self):
        print(self.query_buffer)
        return self.query_buffer.endswith('\n')

    def read_from_conn(self):
        raw_read_data = self.conn.handle_read()
        self.query_buffer += raw_read_data
        if self.is_command_input_end():
            self.query_cursor += len(self.query_buffer)
            self.read_data = RESProtocol(self.query_buffer).parse()
            self.query_buffer = ''
            self.query_cursor = 0

    def read_from_client(self):
        self.read_from_conn()
        read_data = self.read_data
        if not read_data: return
        self.slave_check(read_data)
        self.handle_command(read_data)
        self.conn.enable_write()
        self.read_data = ''

    def write_to_client(self):
        while len(self.reply_buffer):
            data = self.reply_buffer.pop()
            self.conn.handle_write(data)
            self.conn.enable_read()

    def append_reply(self, reply):
        self.reply_buffer.appendleft(reply)

    def handle_command_after_resp(self, cmd_data):
        cmd_data = RESProtocol(cmd_data).parse()
        self.handle_command(cmd_data)

    def handle_command(self, cmd_data):
        handler = CommandHandler(self, cmd_data)
        handler.handle()

    # def switch_database(self, db_index):
    #     self.db = server.get_database(db_index)
    #
    def get_server(self):
        return self.server

    def set_current_command(self, command: BaseCommand) -> bool:
        self.current_command = command
        if command is None: return False

        if command.cmd_type & CommandType.CMD_WRITE:
            # write command ++
            self.server.write_cmd_increment()
            # AOF buffer
            self.server.aof_buf.append(command.raw_cmd)
            # sender write command to connected slaves
            self.send_write_cmd_to_slave(command.raw_cmd)
        elif self.server.repl_slave_ro and \
            command.cmd_type & CommandType.CMD_READ and \
            self.repl_state == REPL_SLAVE_STATE.NONE:
            print('readable', command.raw_cmd)
            if self.slave_handle_command(command):
                return False
        return True

    def slave_handle_command(self, command: BaseCommand) -> bool:
        slave = self.server.select_slave()
        if slave:
            slave.origin_cmd_sender = self
            slave.append_reply(f'{command.raw_cmd}\n')
            slave.conn.enable_write()
            return True
        return False

    def send_write_cmd_to_slave(self, cmd_data):
        slaves = self.server.get_connected_slaves()
        for slave in slaves:
            slave.append_reply(f'{cmd_data}\n')
            slave.conn.enable_write()

    def slave_check(self, read_data):
        if read_data.startswith('REPLCONF listening-port'.lower()):
            self.repl_state = REPL_SLAVE_STATE.RECEIVE_PORT
            self.server.upgrade_client_to_master(self)
        elif read_data.startswith('REPLCONF ip-address'.lower()):
            self.repl_state = REPL_SLAVE_STATE.RECEIVE_IP
        elif read_data.startswith('SYNC'.lower()):
            self.repl_state = REPL_SLAVE_STATE.RECEIVE_PSYNC
        elif read_data.startswith('(ok)'.lower()):
            if self.repl_state == REPL_SLAVE_STATE.RECEIVE_PSYNC:
                self.repl_state = REPL_SLAVE_STATE.TRANSFER
                print('TRANSFER')
            elif self.repl_state == REPL_SLAVE_STATE.TRANSFER:
                self.repl_state = REPL_SLAVE_STATE.CONNECTED
                print('CONNECTED')
