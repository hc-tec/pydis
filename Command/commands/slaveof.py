
from Generic.socket import socket_connect
from Command.base import BaseCommand, CommandType
from Exception.socket import ConnectionRefuseError
from Replication.base import REPL_SLAVE_STATE
from Conf.command import CMD_RES
from Replication.interfaces import IReplServerSlaveManager


class SlaveOf(BaseCommand):
    '''
    slaveof 127.0.0.1 9527
    '''

    args_order = ['host', 'port']
    min_args = 2
    max_args = 2
    cmd_type = CommandType.CMD_COMMON

    def handle(self, args, kwargs):
        server = self.client.get_server()
        host = kwargs['host']
        port = int(kwargs['port'])
        repl_slave_manager: IReplServerSlaveManager = server.get_repl_slave_manager()
        repl_slave_manager.set_addr(host, port)
        try:
            repl_slave_manager.set_repl_state(REPL_SLAVE_STATE.CONNECT)
            slave_conn = socket_connect(host, port)
            repl_slave_manager.set_repl_state(REPL_SLAVE_STATE.CONNECTING)
            server.connect_to_master(slave_conn, self.client)
            return CMD_RES.WAIT
        except TypeError as e:
            print(e)
            repl_slave_manager.set_repl_state(REPL_SLAVE_STATE.NONE)
            repl_slave_manager.set_addr(None, None)
            raise ConnectionRefuseError(host, port)
