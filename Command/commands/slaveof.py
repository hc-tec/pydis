
from Generic.socket import socket_connect
from Command.base import BaseCommand, CommandType
from Exception.socket import ConnectionRefuseError
from Replication.base import REPL_SLAVE_STATE
from Conf.command import CMD_RES


class SlaveOf(BaseCommand):
    '''
    slaveof 127.0.0.1 9527
    '''

    args_order = ['host', 'port']
    min_args = 2
    max_args = 2
    cmd_type = CommandType.CMD_COMMON

    def handle(self, args, kwargs):
        server = self.client.server
        server.master_host = kwargs['host']
        server.master_port = int(kwargs['port'])
        try:
            server.repl_state = REPL_SLAVE_STATE.CONNECT
            slave_conn = socket_connect(server.master_host, server.master_port)
            server.repl_state = REPL_SLAVE_STATE.CONNECTING
            server.connect_to_master(slave_conn, (server.master_host, server.master_port), self.client)
            # blocking slaveof command, append command sender to blocking_dict
            return CMD_RES.WAIT
        except TypeError as e:
            print(e)
            server.repl_state = REPL_SLAVE_STATE.NONE
            server.master_host = None
            server.master_port = None
            raise ConnectionRefuseError(server.master_host, server.master_port)

