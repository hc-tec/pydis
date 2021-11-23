
import socket

from Connection.interfaces import IConnection
from IOLoop.Reactor.interfaces import IAcceptor
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

    def connected(self) -> int:
        conn, addr = self.__socket.accept()
        conn.setblocking(False)
        server.connect_from_client(conn)
        return conn.fileno()

    def data_received(self, fd: int) -> IConnection:
        return server.read_from_client(fd)

    def ready_to_write(self, fd: int) -> IConnection:
        return server.write_to_client(fd)

    def connect_close(self, fd: int):
        pass

