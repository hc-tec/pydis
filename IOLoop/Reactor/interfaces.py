
from abc import ABCMeta, abstractmethod

from interfaces import Factory
from Connection.interfaces import IConnection
from Timer.interfaces import ITimerManager
from IOLoop.Reactor.poller.interfaces import IPoller


class IAcceptor(metaclass=ABCMeta):

    @abstractmethod
    def listen_socket(self):
        ...

    @abstractmethod
    def listen_fd(self):
        ...

    @abstractmethod
    def connected(self) -> int:
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


class IReactor(ITimerManager):

    @abstractmethod
    def get_acceptor(self) -> IAcceptor:
        ...

    @abstractmethod
    def get_poller(self) -> IPoller:
        ...

    @abstractmethod
    def event_change(self, fd, event):
        ...

    @abstractmethod
    def process_poll_event(self, events):
        ...

    @abstractmethod
    def poll(self):
        ...





class IAcceptorFactory(Factory):

    @abstractmethod
    def build(self, host: str, port: int):
        ...

