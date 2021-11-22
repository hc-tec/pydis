
from abc import ABCMeta, abstractmethod


class Poller(metaclass=ABCMeta):

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


