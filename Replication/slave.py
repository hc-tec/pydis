
from Client import Client
from Replication.base import REPL_SLAVE_STATE


class SLAVE_STATE:
    WAIT_BGSAVE_START = 0
    WAIT_BGSAVE_END = 1 << 0
    SEND_BULK = 1 << 1
    ONLINE = 1 << 2


class SlaveClient(Client):

    def __init__(self, *args, **kwargs):
        self.origin_client: Client = kwargs.pop('origin_client')
        super().__init__(*args, **kwargs)
        self.replicate()

    def is_persistence_data(self, data):
        return data.startswith('[')

    def read_from_client(self):
        read_data = self.read_from_conn()
        if read_data is None: return
        server = self.server
        if server.repl_state == REPL_SLAVE_STATE.CONNECTED:
            print('slave handler', read_data)
            self.handle_command(read_data)
            self.conn.enable_write()
            return
        if read_data == 'pong':
            server.repl_state = REPL_SLAVE_STATE.RECEIVE_PONG
        elif read_data == '(ok)':
            if server.repl_state == REPL_SLAVE_STATE.RECEIVE_IP:
                server.repl_state = REPL_SLAVE_STATE.SEND_PSYNC
            elif server.repl_state == REPL_SLAVE_STATE.RECEIVE_PSYNC:
                pass
            else:
                server.repl_state += 1
        elif self.is_persistence_data(read_data):
            server.repl_state = REPL_SLAVE_STATE.TRANSFER
            server.load_from_master(read_data)
            server.repl_state = REPL_SLAVE_STATE.CONNECTED
            print(read_data)
            # tell slaveof command sender all works are finish

            server.master.append_reply('(ok)\n')
            server.master.conn.enable_write()
            self.origin_client.append_reply('(ok)\n')
            self.origin_client.conn.enable_write()
            self.origin_client = None

        if server.repl_state < REPL_SLAVE_STATE.TRANSFER:
            self.replicate()

    def replicate(self):
        server = self.server
        if server.repl_state == REPL_SLAVE_STATE.CONNECTING:
            self.append_reply('PING\n')
        elif server.repl_state == REPL_SLAVE_STATE.RECEIVE_PONG:
            # self.append_reply('')
            server.repl_state = REPL_SLAVE_STATE.SEND_PORT
        if server.repl_state == REPL_SLAVE_STATE.SEND_PORT:
            self.append_reply('REPLCONF listening-port {}\n'.format(
                server.port
            ))
            server.repl_state = REPL_SLAVE_STATE.RECEIVE_PORT
        elif server.repl_state == REPL_SLAVE_STATE.SEND_IP:
            self.append_reply('REPLCONF ip-address {}\n'.format(
                server.host
            ))
            server.repl_state = REPL_SLAVE_STATE.RECEIVE_IP
        elif server.repl_state == REPL_SLAVE_STATE.SEND_PSYNC:
            self.append_reply('SYNC\n')
            server.repl_state = REPL_SLAVE_STATE.RECEIVE_PSYNC
        elif server.repl_state == REPL_SLAVE_STATE.RECEIVE_PSYNC:
            self.append_reply('(ok)\n')
            server.repl_state = REPL_SLAVE_STATE.TRANSFER
        self.conn.enable_write()
