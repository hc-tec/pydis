
from Command.base import BaseCommand, CommandType
from Conf.command import CMD_RES


class BgSave(BaseCommand):

    args_order = []
    cmd_type = CommandType.CMD_COMMON

    def handle(self, args):
        self.client.server.rdb_start()
        return CMD_RES.OK
