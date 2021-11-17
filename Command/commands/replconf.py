
from Command.base import BaseCommand, CommandType
from Conf.command import CMD_RES

class ReplConf(BaseCommand):

    args_order = ['key', 'value']
    min_args = 2
    max_args = 2
    cmd_type = CommandType.CMD_COMMON

    def handle(self, args):
        return CMD_RES.OK
