
from abc import abstractmethod


class Poller:

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


