

from Pubsub.case import Pubsub
from Client.base import CLIENT_FLAG
from Command.base import BaseCommand, CommandType
from Conf.command import CMD_RES


class Unsubscribe(BaseCommand):
    '''
    subscribe channel
    '''
    need_kwargs = False
    cmd_type = CommandType.CMD_COMMON

    def handle(self, args, kwargs):
        if not args:
            Pubsub.unsubscribeAll(self.client)
        for channel_name in args:
            Pubsub.unsubscribe(self.client, channel_name)
        if not self.client.pubsub_channels:
            self.client.flag &= ~CLIENT_FLAG.PUBSUB
        if self.client.reply_buffer:
            self.client.conn.enable_write()
        return CMD_RES.WAIT
