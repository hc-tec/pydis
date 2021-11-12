
import socket
import select

# from IOLoop.Reactor.Reactor import Reactor
from IOLoop.Reactor.FileEvent import FileEvent
from IOLoop.Reactor.FiredEvent import FiredEvent


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

    def accept(self):
        conn, addr = self.__socket.accept()
        conn.setblocking(False)
        conn_fd = conn.fileno()
        file_event = FileEvent(self.reactor, conn, addr)
        self.reactor.events[conn_fd] = file_event
        self.reactor.poller.register(conn_fd, select.EPOLLIN)

    def handle_read(self, fired_event: FiredEvent):
        file_event = self.reactor.events[fired_event.fd]
        file_event.read()
        self.reactor.poller.modify(fired_event.fd, select.EPOLLOUT)

    def handle_write(self, fired_event: FiredEvent):
        file_event = self.reactor.events[fired_event.fd]
        file_event.write()
        self.reactor.poller.modify(fired_event.fd, select.EPOLLIN)

    def handle_close(self, fired_event: FiredEvent):
        self.reactor.poller.unregister(fired_event.fd)

