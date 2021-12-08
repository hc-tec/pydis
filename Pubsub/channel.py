

from Pubsub.interfaces import IChannel


class Channel(IChannel):

    def __init__(self, channel_name: str):
        super().__init__()
        self.channel_name = channel_name

    def get_subscribe_message(self):
        return f'subscribe\n' \
            f'{self.channel_name}\n' \
            f'{self.get_observers_num()}\n'

    def get_unsubscribe_message(self):
        return f'unsubscribe\n' \
            f'{self.channel_name}\n' \
            f'{self.get_observers_num()}\n'

    def get_publish_message(self, message):
        return f'message\n' \
                        f'{self.channel_name}\n' \
                        f'{message}\n'

    def get_observers_num(self):
        return len(self._observers)
