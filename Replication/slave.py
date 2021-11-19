
from Client import Client
from Replication.base import REPL_SLAVE_STATE


class SLAVE_STATE:
    WAIT_BGSAVE_START = 0
    WAIT_BGSAVE_END = 1 << 0
    SEND_BULK = 1 << 1
    ONLINE = 1 << 2


class SlaveClient(Client):

    def __init__(self, *args, **kwargs):
        self.slaveof_cmd_sender: Client = kwargs.pop('slaveof_cmd_sender')
        super().__init__(*args, **kwargs)
        self.replicate()

    def is_persistence_data(self, data):
        return data.startswith('[')

    def read_from_client(self):
        self.read_from_conn()
        read_data = self.read_data
        if not read_data: return
        server = self.server
        if server.repl_state == REPL_SLAVE_STATE.CONNECTED:
            print('slave handle command from master: ', read_data)
            self.handle_command(read_data)
            self.conn.enable_write()
            return
        self.check_master_reply(read_data)

        # when enter TRANSFER state, replicate() can't be executed
        if server.repl_state < REPL_SLAVE_STATE.TRANSFER:
            self.replicate()
        self.read_data = ''

    def replicate(self):
        server = self.server
        if server.repl_state == REPL_SLAVE_STATE.CONNECTING:
            self.append_reply('PING\n')
        elif server.repl_state == REPL_SLAVE_STATE.RECEIVE_PONG:
            # self.append_reply('')
            server.repl_state = REPL_SLAVE_STATE.SEND_PORT
        elif server.repl_state == REPL_SLAVE_STATE.SEND_PORT:
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

    def check_master_reply(self, read_data):
        server = self.server
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
            server.load_from_master(read_data)
            server.repl_state = REPL_SLAVE_STATE.CONNECTED
            server.master.append_reply('(ok)\n')
            server.master.conn.enable_write()
            # tell slaveof command sender all works are finish
            self.slaveof_cmd_sender.append_reply('(ok)\n')
            self.slaveof_cmd_sender.conn.enable_write()
            self.slaveof_cmd_sender = None


