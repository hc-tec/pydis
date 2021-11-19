
from Command.base import BaseCommand, CommandType
from Conf.command import CMD_RES
from Client.base import CLIENT_FLAG


class Multi(BaseCommand):

    args_order = []
    min_args = 0
    max_args = 0
    cmd_type = CommandType.CMD_COMMON

    def handle(self, args, kwargs):
        self.client.flag |= CLIENT_FLAG.MULTI
        return CMD_RES.OK
