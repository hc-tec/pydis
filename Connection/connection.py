
from socket import socket

from IOLoop import IOReader, IOWriter
from IOLoop.Reactor import reactor
from IOLoop.Reactor.firedEvent import ReEvent
from Connection.interfaces import IConnection


class Connection(IConnection):

    def __init__(self, sock: socket, reactor: reactor):
        self.__socket = sock
        self.__reactor: reactor = reactor
        self.__event = ReEvent.RE_READABLE

    @property
    def sock_fd(self):
        return self.__socket.fileno()

    def handle_read(self) -> str:
        read_data = IOReader.read_from_socket(self.__socket)
        if read_data == '':
            self.handle_close()
        return read_data

    def handle_write(self, data) -> int:
        return IOWriter.write_to_socket(self.__socket, data)

    def handle_close(self):
        try:
            self.__reactor.poller.unregister(self.sock_fd)
            self.__socket.close()
        except Exception:
            pass

    def enable_read(self):
        self.update_event(ReEvent.RE_READABLE)

    def enable_write(self):
        self.update_event(ReEvent.RE_WRITABLE)

    def update_event(self, event):
        self.__event = event
        self._update_poller()

    def _update_poller(self):
        self.__reactor.poller.modify(self.sock_fd, self.__event)

    def register(self):
        self.__reactor.poller.register(self.sock_fd, self.__event)
