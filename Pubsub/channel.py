

from Pubsub.interfaces import IChannel


class Channel(IChannel):

    def __init__(self, channel_name: str):
        super().__init__()
        self.channel_name = channel_name
        self.message = self.set_subscribe_message()

    def set_subscribe_message(self):
        self.message = f'subscribe\n' \
            f'{self.channel_name}\n' \
            f'{self.get_observers_num()}\n'

    def get_unsubscribe_message(self):
        return f'unsubscribe\n' \
            f'{self.channel_name}\n' \
            f'{self.get_observers_num()}\n'

    def set_publish_message(self, message):
        self.message = f'message\n' \
                        f'{self.channel_name}\n' \
                        f'{message}\n'

    def get_observers_num(self):
        return len(self._observers)
