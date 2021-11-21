
from abc import ABCMeta, abstractmethod
from IOLoop.Reactor.firedEvent import FiredEvent


class IReactor(metaclass=ABCMeta):

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


class IReactorManager(metaclass=ABCMeta):

    @abstractmethod
    def set_loop(self, loop: IReactor):
        ...

    @abstractmethod
    def get_loop(self):
        ...


class IPoller(metaclass=ABCMeta):

    @abstractmethod
    def register(self, fd, event):
        pass

    @abstractmethod
    def unregister(self, fd):
        pass

    @abstractmethod
    def modify(self, fd, event):
        pass

    @abstractmethod
    def poll(self, reactor, timeout=None):
        pass


class IAcceptor(metaclass=ABCMeta):

    @abstractmethod
    def listen_socket(self):
        ...

    @abstractmethod
    def listen_fd(self):
        ...

    @abstractmethod
    def handle_accept(self, events, poller: IPoller):
        ...

    @abstractmethod
    def handle_read(self, fired_event: FiredEvent):
        ...

    @abstractmethod
    def handle_write(self, fired_event: FiredEvent):
        ...

    @abstractmethod
    def handle_close(self, poller: IPoller, fired_event: FiredEvent):
        ...

