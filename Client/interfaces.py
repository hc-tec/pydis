
from abc import ABCMeta, abstractmethod


class IClient(metaclass=ABCMeta):

    @abstractmethod
    def get_server(self):
        ...


class IResponse(metaclass=ABCMeta):

    @abstractmethod
    def append_reply(self, reply):
        ...

