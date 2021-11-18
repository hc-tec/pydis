

from Client.client import Client
from Replication.base import REPL_SLAVE_STATE



class MasterClient(Client):

    def __init__(self):
        super().__init__(None, None, None, None)

    def upgrade_from_client(self, client: Client):
        property_list = client.__dict__.keys()
        for property in property_list:
            setattr(self, property, getattr(client, property))

    def read_from_client(self):
        print('master now')
        read_data = self.read_from_conn()
        if read_data is None: return
        if self.handle_client:
            self.handle_client.append_reply(f'{read_data}\n')
            self.handle_client.conn.enable_write()
            self.handle_client = None
            return
        if self.repl_state == REPL_SLAVE_STATE.CONNECTED: return

        self.slave_check(read_data)
        self.handle_command(read_data)
        self.conn.enable_write()

    def slave_check(self, read_data: str):
        if read_data.startswith('REPLCONF ip-address'.lower()):
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


