
from abc import ABCMeta, abstractmethod
from interfaces import Factory


class ITimestamp(metaclass=ABCMeta):

    @abstractmethod
    def get_time(self):
        ...


class ITimeoutEvent(metaclass=ABCMeta):

    @abstractmethod
    def get_timestamp(self) -> ITimestamp:
        ...

    @abstractmethod
    def set_extra_data(self, extra_data):
        ...

    @abstractmethod
    def handle_event(self, reactor):
        ...


class ITimer(metaclass=ABCMeta):

    @abstractmethod
    def get_events(self):
        ...

    @abstractmethod
    def add_event(self, event: ITimeoutEvent):
        ...

    @abstractmethod
    def pop_event(self) -> ITimeoutEvent:
        ...

    @abstractmethod
    def get_earliest_time(self):
        ...

    @abstractmethod
    def is_event_can_active(self):
        ...

class ITimerManager(metaclass=ABCMeta):

    @abstractmethod
    def create_timeout_event(self, timeout_event: ITimeoutEvent):
        ...

    @abstractmethod
    def get_earliest_time(self):
        ...

    @abstractmethod
    def process_timer_event(self):
        ...


class ITimerFactory(Factory):

    @abstractmethod
    def build(self) -> ITimer:
        ...
