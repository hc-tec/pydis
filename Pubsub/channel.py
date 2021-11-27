

from Pubsub.interfaces import IChannel


class Channel(IChannel):

    def __init__(self, channel_name: str):
        super().__init__()
        self.channel_name = channel_name
        self.message = self.set_subscribe_message()

    def set_subscribe_message(self):
        self.message = f'1) subscribe\n' \
            f'2) {self.channel_name}\n' \
            f'3) {self.get_observers_num()}\n'

    def get_unsubscribe_message(self):
        return f'1) unsubscribe\n' \
            f'2) {self.channel_name}\n' \
            f'3) {self.get_observers_num()}\n'

    def set_publish_message(self, message):
        self.message = f'1) message\n' \
                        f'2) {self.channel_name}\n' \
                        f'3) {message}\n'

    def get_observers_num(self):
        return len(self._observers)
