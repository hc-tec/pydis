
from Pubsub.case import Pubsub
from Command.base import BaseCommand, CommandType


class Publish(BaseCommand):

    args_order = ['channel_name', 'message']
    cmd_type = CommandType.CMD_COMMON

    def handle(self, args, kwargs):
        receivers = Pubsub.publish(self.client, kwargs['channel_name'], kwargs['message'])
        return f'(integer) {receivers}'
