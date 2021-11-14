
from socket import socket
from abc import abstractmethod

from IOLoop import IOReader, IOWriter


class BaseConnection:

    @abstractmethod
    def handle_read(self) -> str:
        ...

    @abstractmethod
    def handle_write(self, data):
        ...


class Connection(BaseConnection):

    def __init__(self, sock: socket):
        self.socket = sock

    def handle_read(self) -> str:
        return IOReader.read_from_socket(self.socket)

    def handle_write(self, data):
        IOWriter.write_to_socket(self.socket, data)

