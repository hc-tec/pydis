

from Command.interfaces import ICommand
from Client.interfaces import IClientHandler, IClient, IMasterHandler, ISlaveHandler
from Replication.base import REPL_SLAVE_STATE
from Command.base import CommandType
from Replication.interfaces import IReplClientManager, IReplServerSlaveManager


class BaseHandler(IClientHandler):

    def handle_command(self, data, client: IClient):
        client.handle_command(data)
        client.get_connection().enable_write()
        client.get_reader().clear_read_data()

    def data_received(self, data, client: IClient):

        self.slave_check(data, client)
        self.handle_command(data, client)

    def check_write(self, command: ICommand, client: IClient):

        if command.cmd_type & CommandType.CMD_WRITE:
            # write command ++
            client.get_server().write_cmd_increment()
            # AOF buffer
            client.get_server().get_aof_manager().append_to_buffer(command.raw_cmd)
            # watch keys change
            client.touch_watched_key(command)
            return True
        return False

    def command_executed_before(self, command: ICommand, client: IClient) -> bool:
        if command is None: return False

        if self.check_write(command, client):
            # sender write command to connected slaves
            self.send_write_cmd_to_slave(command.raw_cmd, client)
        elif client.get_server().get_repl_slave_manager().is_repl_slave_readonly() and \
                command.cmd_type & CommandType.CMD_READ and \
                client.get_server().get_repl_slave_manager().get_repl_state() == REPL_SLAVE_STATE.NONE:
            print('readable', command.raw_cmd)
            if self.slave_handle_command(command, client):
                return False
        return True

    def slave_check(self, read_data, client: IClient):
        if read_data.startswith('REPLCONF listening-port'.lower()):
            client.get_repl_manager().set_repl_state(REPL_SLAVE_STATE.RECEIVE_PORT)
            client.transform_handler(MasterHandler())
            client.get_server().get_repl_master_manager().append_slaves(client)

    def slave_handle_command(self, command: ICommand, client) -> bool:
        slave = client.get_server().get_repl_master_manager().select_slave()
        if slave:
            slave.get_handler().set_origin_cmd_sender(client)
            slave.append_reply_enable_write(f'{command.raw_cmd}\n')
            return True
        return False

    def send_write_cmd_to_slave(self, cmd_data, client):
        slaves = client.get_server().get_repl_master_manager().get_connected_slaves()
        for slave in slaves:
            slave.append_reply_enable_write(f'{cmd_data}\n')


class MasterHandler(BaseHandler, IMasterHandler):

    def __init__(self):
        self._origin_cmd_sender = None

    def set_origin_cmd_sender(self, origin_cmd_sender):
        self._origin_cmd_sender = origin_cmd_sender

    def get_origin_cmd_sender(self):
        return self._origin_cmd_sender

    def data_received(self, data, client):
        read_data: str = data
        if self._origin_cmd_sender:
            print('origin sender')
            self._origin_cmd_sender.append_reply_enable_write(f'{read_data}\n')
            self._origin_cmd_sender = None
            return

        if read_data.__contains__('not exist'):
            client.get_connection().enable_write()
            return
        self.handle_command(read_data, client)

        if client.get_repl_manager().get_repl_state() == REPL_SLAVE_STATE.CONNECTED:
            self.ping_ack(read_data, client)
            return
        else:
            self.slave_check(read_data, client)

    def ping_ack(self, read_data, client):
        if read_data == 'pong':
            client.get_repl_manager().update_repl_ack_time()

    def slave_check(self, read_data, client: IClient):
        repl_manager: IReplClientManager = client.get_repl_manager()
        repl_state = repl_manager.get_repl_state()
        if read_data.startswith('REPLCONF ip-address'.lower()):
            repl_manager.set_repl_state(REPL_SLAVE_STATE.RECEIVE_IP)
        elif read_data.startswith('SYNC'.lower()):
            repl_manager.set_repl_state(REPL_SLAVE_STATE.RECEIVE_PSYNC)
        elif read_data.startswith('(ok)'.lower()):
            if repl_state == REPL_SLAVE_STATE.RECEIVE_PSYNC:
                repl_manager.set_repl_state(REPL_SLAVE_STATE.TRANSFER)
                client.get_server().get_repl_master_manager().sync_enable()
                print('TRANSFER')
            elif repl_state == REPL_SLAVE_STATE.TRANSFER:
                repl_manager.set_repl_state(REPL_SLAVE_STATE.CONNECTED)
                print('CONNECTED')


class SlaveHandler(BaseHandler, ISlaveHandler):

    def __init__(self):
        self._slaveof_cmd_sender = None

    def set_slaveof_cmd_sender(self, slaveof_cmd_sender: IClient):
        self._slaveof_cmd_sender = slaveof_cmd_sender

    def is_persistence_data(self, data):
        return data.startswith('[')

    def data_received(self, data, client: IClient):
        server = client.get_server()
        repl_slave_manager: IReplServerSlaveManager = server.get_repl_slave_manager()
        repl_state = repl_slave_manager.get_repl_state()
        print(repl_state)
        if repl_state == REPL_SLAVE_STATE.CONNECTED:
            if client == repl_slave_manager.get_master():
                print('slave handle command from master: ', data)
            self.handle_command(data, client)
            return
        self.check_master_reply(data, client)

        # when enter TRANSFER state, replicate() can't be executed
        if repl_state < REPL_SLAVE_STATE.TRANSFER:
            self.replicate(client)
        # else:
        #     client.get_connection().enable_read()

    def replicate(self, client: IClient):
        server = client.get_server()
        repl_manager = server.get_repl_slave_manager()
        repl_state = repl_manager.get_repl_state()
        if repl_state == REPL_SLAVE_STATE.CONNECTING:
            client.append_reply_enable_write('PING\n')
        elif repl_state == REPL_SLAVE_STATE.RECEIVE_PONG:
            # self.append_reply('')
            repl_manager.set_repl_state(REPL_SLAVE_STATE.SEND_PORT)
        elif repl_state == REPL_SLAVE_STATE.SEND_PORT:
            client.append_reply_enable_write('REPLCONF listening-port {}\n'.format(
                server.get_addr()['port']
            ))
            repl_manager.set_repl_state(REPL_SLAVE_STATE.RECEIVE_PORT)
        elif repl_state == REPL_SLAVE_STATE.SEND_IP:
            client.append_reply_enable_write('REPLCONF ip-address {}\n'.format(
                server.get_addr()['host']
            ))
            repl_manager.set_repl_state(REPL_SLAVE_STATE.RECEIVE_IP)
        elif repl_state == REPL_SLAVE_STATE.SEND_PSYNC:
            client.append_reply_enable_write('SYNC\n')
            repl_manager.set_repl_state(REPL_SLAVE_STATE.RECEIVE_PSYNC)
        elif repl_state == REPL_SLAVE_STATE.RECEIVE_PSYNC:
            client.append_reply_enable_write('(ok)\n')
            repl_manager.set_repl_state(REPL_SLAVE_STATE.TRANSFER)

    def check_master_reply(self, read_data, client: IClient):
        server = client.get_server()
        repl_manager = server.get_repl_slave_manager()
        repl_state = repl_manager.get_repl_state()
        if read_data == 'pong':
            repl_manager.set_repl_state(REPL_SLAVE_STATE.SEND_PORT)
        elif read_data == '(ok)':
            if repl_state == REPL_SLAVE_STATE.RECEIVE_IP:
                repl_manager.set_repl_state(REPL_SLAVE_STATE.SEND_PSYNC)
            elif repl_state == REPL_SLAVE_STATE.RECEIVE_PSYNC:
                pass
            elif repl_state == REPL_SLAVE_STATE.TRANSFER:
                pass
            else:
                print(repl_state)
                repl_manager.set_repl_state(repl_state+1)
        elif self.is_persistence_data(read_data):
            server.get_rdb_manager().load_from_master(server.get_database_manager(), read_data)
            repl_manager.set_repl_state(REPL_SLAVE_STATE.CONNECTED)

            server.get_repl_slave_manager().get_master().append_reply_enable_write('(ok)\n')
            # tell slaveof command sender all works are finish
            self._slaveof_cmd_sender.append_reply_enable_write('(ok)\n')
            self._slaveof_cmd_sender = None


