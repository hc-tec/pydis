
import socket
import select

# from IOLoop.Reactor.Reactor import Reactor
from IOLoop.Reactor.FileEvent import FileEvent
from IOLoop.Reactor.FiredEvent import FiredEvent, ReEvent
from Server import server


class Acceptor:

    def __init__(self, ip, port, reactor):
        self.reactor = reactor
        self.ip = ip
        self.port = port
        self.__create_socket()

    def __create_socket(self):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__socket.bind((self.ip, self.port))
        self.__socket.listen(1024)
        self.__socket.setblocking(False)

    def listen_socket(self):
        return self.__socket

    def listen_fd(self):
        return self.__socket.fileno()

    def handle_accept(self):
        conn, addr = self.__socket.accept()
        conn.setblocking(False)
        conn_fd = conn.fileno()
        file_event = FileEvent(self.reactor, conn, addr)
        self.reactor.events[conn_fd] = file_event
        self.reactor.poller.register(conn_fd, ReEvent.RE_READABLE)

        server.connect_from_client(conn)

    def handle_read(self, fired_event: FiredEvent):
        server.read_from_client(fired_event.fd)

    def handle_write(self, fired_event: FiredEvent):
        server.write_to_client(fired_event.fd)

    def handle_close(self, fired_event: FiredEvent):
        self.reactor.poller.unregister(fired_event.fd)

