
from socket import socket

from IOLoop import IOReader, IOWriter
from IOLoop.Reactor.event import ReEvent
from Connection.interfaces import IConnection


class Connection(IConnection):

    def __init__(self, sock: socket):
        self.__socket = sock
        self.__event = ReEvent.RE_READABLE

    def get_event(self):
        return self.__event

    def get_sock_fd(self):
        return self.__socket.fileno()

    def data_received(self) -> str:
        read_data = IOReader.read_from_socket(self.__socket)
        if read_data == '':
            self.connect_close()
        return read_data

    def ready_to_write(self, data) -> int:
        return IOWriter.write_to_socket(self.__socket, data)

    def connect_close(self):
        try:
            self.update_event(ReEvent.RE_CLOSE)
            self.__socket.close()
        except Exception:
            pass

    def enable_read(self):
        self.update_event(ReEvent.RE_READABLE)

    def enable_write(self):
        self.update_event(ReEvent.RE_WRITABLE)

    def update_event(self, event):
        self.__event = event
