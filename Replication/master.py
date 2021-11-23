

from Client.client import Client
from Replication.base import REPL_SLAVE_STATE
from Generic.time import get_cur_time


class MasterClient(Client):

    def __init__(self):
        super().__init__(None, None, None, None)
        self.origin_cmd_sender = None  # the READ command sender slave handle

    def upgrade_from_client(self, client: Client):
        property_list = client.__dict__.keys()
        for property in property_list:
            setattr(self, property, getattr(client, property))

    def read_from_client(self):
        print('master now')
        self.read_from_conn()
        read_data = self.read_data
        if not read_data: return
        if self.origin_cmd_sender:
            print('origin sender')
            self.origin_cmd_sender.append_reply_enable_write(f'{read_data}\n')
            self.origin_cmd_sender = None
            return
        if self.repl_state == REPL_SLAVE_STATE.CONNECTED:
            self.ping_ack(read_data)
            return
        if read_data.startswith('Command is not exist'):
            return
        self.slave_check(read_data)
        self.handle_command(read_data)
        self.conn.enable_write()
        self.read_data = ''

    def ping_ack(self, read_data):
        print('ping ack')
        if read_data == 'pong':
            self.repl_ack_time = get_cur_time()
