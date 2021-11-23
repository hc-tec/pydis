
from Command.base import BaseCommand, CommandType
from Conf.command import CMD_RES


class BgSave(BaseCommand):

    args_order = []
    cmd_type = CommandType.CMD_COMMON

    def handle(self, args, kwargs):
        self.client.get_server().start_rdb()
        return CMD_RES.OK
