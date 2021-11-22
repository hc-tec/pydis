

from abc import ABCMeta, abstractmethod
from interfaces import Factory


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
    def poll(self, timeout=None):
        pass


class IPollerFactory(Factory):

    @abstractmethod
    def build(self) -> IPoller:
        ...
