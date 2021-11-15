
from Timer.timestamp import Timestamp


class TimeoutEvent:

    def __init__(self, timestamp: Timestamp):
        self.__timestamp = timestamp

    def get_timestamp(self):
        return self.__timestamp

    def __gt__(self, other):
        return self.get_timestamp().get_time() > other.get_timestamp().get_time()

    def __ge__(self, other):
        return self.get_timestamp().get_time() >= other.get_timestamp().get_time()

    def __lt__(self, other):
        return self.get_timestamp().get_time() < other.get_timestamp().get_time()

    def __le__(self, other):
        return self.get_timestamp().get_time() <= other.get_timestamp().get_time()

    def __str__(self):
        return f'<TimeoutEvent timestamp={int(self.get_timestamp().get_time())}>'

    __repr__ = __str__


