
from socket import socket
from abc import ABCMeta, abstractmethod


class IServer(metaclass=ABCMeta):

    # @abstractmethod
    # def connect_from_client(self, conn: socket):
    #     ...

    @abstractmethod
    def start_watchdog(self):
        ...

