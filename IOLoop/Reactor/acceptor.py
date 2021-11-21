
import socket

from IOLoop.Reactor.fileEvent import FileEvent
from IOLoop.Reactor.firedEvent import FiredEvent, ReEvent
from IOLoop.Reactor.poller.base import Poller
from IOLoop.interfaces import IAcceptor
from Server.server import server


class Acceptor(IAcceptor):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.__create_socket()

    def __create_socket(self):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__socket.bind((self.host, self.port))
        self.__socket.listen(1024)
        self.__socket.setblocking(False)

    def listen_socket(self):
        return self.__socket

    def listen_fd(self):
        return self.__socket.fileno()

    def handle_accept(self, events, poller: Poller):
        conn, addr = self.__socket.accept()
        conn.setblocking(False)
        self._handle_accept(conn, addr, events, poller)
        server.connect_from_client(conn)

    def _handle_accept(self, conn, addr, events, poller: Poller):
        conn_fd = conn.fileno()
        file_event = FileEvent(conn, addr)
        events[conn_fd] = file_event
        poller.register(conn_fd, ReEvent.RE_READABLE)

    def handle_read(self, fired_event: FiredEvent):
        server.read_from_client(fired_event.fd)

    def handle_write(self, fired_event: FiredEvent):
        server.write_to_client(fired_event.fd)

    def handle_close(self, poller: Poller, fired_event: FiredEvent):
        poller.unregister(fired_event.fd)

