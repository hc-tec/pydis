
from abc import ABCMeta, abstractmethod

from interfaces import Factory
from Connection.interfaces import IConnection
from Timer.interfaces import ITimerManager


class IReactor(ITimerManager):

    @abstractmethod
    def get_acceptor(self):
        ...

    @abstractmethod
    def get_poller(self):
        ...

    @abstractmethod
    def process_poll_event(self, events):
        ...

    @abstractmethod
    def poll(self):
        ...


class IAcceptor(metaclass=ABCMeta):

    @abstractmethod
    def listen_socket(self):
        ...

    @abstractmethod
    def listen_fd(self):
        ...

    @abstractmethod
    def connected(self, fd=None) -> int:
        ...

    @abstractmethod
    def data_received(self, fd: int) -> IConnection:
        ...

    @abstractmethod
    def ready_to_write(self, fd: int) -> IConnection:
        ...

    @abstractmethod
    def connect_close(self, fd: int):
        ...


class IAcceptorFactory(Factory):

    @abstractmethod
    def build(self, host: str, port: int):
        ...

