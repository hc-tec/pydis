
from Exception.base import BaseError


class ChannelIsNotExistError(BaseError):

    def __init__(self, channel_name):
        self.msg = f'Channel[{channel_name}] is not exist'



