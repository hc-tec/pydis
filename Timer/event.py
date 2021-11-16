
from typing import Callable
from Timer.timestamp import Timestamp


class TimeoutEvent:

    def __init__(self, timestamp: Timestamp):
        self.__timestamp = timestamp
        # self.__callback = None
        self.extra_data = None

    def get_timestamp(self):
        return self.__timestamp

    # def set_callback(self, callback: Callable):
    #     if callback and callable(callback):
    #         self.__callback = callback
    #     return self

    def set_extra_data(self, extra_data):
        self.extra_data = extra_data
        return self

    def handle_event(self, reactor):
        # self.__callback(reactor, self.__extra_data)
        pass

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


