
from abc import ABCMeta, abstractmethod


class IConnection(metaclass=ABCMeta):

    @abstractmethod
    def get_event(self):
        ...

    @abstractmethod
    def data_received(self) -> str:
        ...

    @abstractmethod
    def ready_to_write(self, data):
        ...

    @abstractmethod
    def connect_close(self):
        ...


class IClosable(metaclass=ABCMeta):

    @abstractmethod
    def close(self):
        ...
