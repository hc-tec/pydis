
from abc import ABCMeta, abstractmethod


class IConnection(metaclass=ABCMeta):

    @abstractmethod
    def handle_read(self) -> str:
        ...

    @abstractmethod
    def handle_write(self, data):
        ...


class IClosable(metaclass=ABCMeta):

    @abstractmethod
    def close(self):
        ...
