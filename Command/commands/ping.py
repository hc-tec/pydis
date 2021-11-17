


from Command.base import BaseCommand, CommandType
from Database import Database


class Ping(BaseCommand):

    args_order = []
    min_args = 0
    max_args = 0
    cmd_type = CommandType.CMD_COMMON

    def handle(self, args):
        return 'PONG'