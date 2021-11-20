

from Pubsub.case import Pubsub
from Client.base import CLIENT_FLAG
from Command.base import BaseCommand, CommandType
from Conf.command import CMD_RES


class Subscribe(BaseCommand):
    '''
    subscribe channel
    '''
    need_kwargs = False
    cmd_type = CommandType.CMD_COMMON

    def handle(self, args, kwargs):

        for channel_name in args:
            Pubsub.subscribe(self.client, channel_name)
        self.client.flag |= CLIENT_FLAG.PUBSUB
        return CMD_RES.WAIT
