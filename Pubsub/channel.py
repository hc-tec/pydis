

from Generic.patterns.observer import Subject


class Channel(Subject):

    def __init__(self, channel_name: str):
        super().__init__()
        self.channel_name = channel_name
        self.message = f'1) subscribe\n' \
                        f'2) {self.channel_name}\n' \
                        f'3) {self.get_observers_num()+1}\n'

    def set_message(self, message):
        self.message = f'1) message\n' \
                        f'2) {self.channel_name}\n' \
                        f'3) {message}\n'

    def get_observers_num(self):
        return len(self._observers)
