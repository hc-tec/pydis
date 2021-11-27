
from Command.base import BaseCommand, CommandType
from Conf.command import CMD_RES


class Info(BaseCommand):
    need_kwargs = False
    cmd_type = CommandType.CMD_READ

    def handle(self, args, kwargs):
        return CMD_RES.OK
