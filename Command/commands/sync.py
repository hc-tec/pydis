
from Command.base import BaseCommand, CommandType
from Conf.command import CMD_RES


class Sync(BaseCommand):

    args_order = []
    cmd_type = CommandType.CMD_COMMON

    def handle(self, args):
        self.client.server.need_sync = True
        self.client.handle_command_after_resp('bgsave')
        return CMD_RES.OK
