
from Command.base import BaseCommand, CommandType
from Command.exception import DiscardWithoutMultiError
from Conf.command import CMD_RES
from Client.base import CLIENT_FLAG



class Discard(BaseCommand):

    args_order = []
    min_args = 0
    max_args = 0
    cmd_type = CommandType.CMD_COMMON

    def handle(self, args, kwargs):
        if self.client.flag & CLIENT_FLAG.MULTI:
            self.client.flag &= ~CLIENT_FLAG.MULTI
            self.client.ms_state.clear()
            return CMD_RES.OK
        else:
            raise DiscardWithoutMultiError()
