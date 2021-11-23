
from Command.base import BaseCommand, CommandType
from Conf.command import CMD_RES


class ReplConf(BaseCommand):
    '''
    :args_order
        :key
            listening-port
            ip-address
    '''
    args_order = ['key', 'value']
    min_args = 2
    max_args = 2
    cmd_type = CommandType.CMD_COMMON

    def handle(self, args, kwargs):
        key_mapping = {
            'listening-port': '_port_as_slave',
            'ip-address': '_host_as_slave'
        }
        setattr(self.client.get_repl_manager(), key_mapping[args[0]], args[1])
        # if 'listening-port' in args:
        #     self.client.port_as_slave = args['value']
        # elif 'ip-address' in args:
        #     self.client.host_as_slave = args['value']
        return CMD_RES.OK
