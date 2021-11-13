
from typing import Dict

from socket import socket
from Client import ReClient
from Connection import Connection


class ReServer:

    def __init__(self):
        self.__next_client_id = 1
        self.__loop = None
        self.__clients: Dict[int, ReClient] = {}
        self.__slaves = []
        self.__monitors = []
        self.__current_client = None

        # RDB / AOF
        self.loading = False

        # Configuration
        self.db_num = 16

        # Limits
        self.max_clients = 1000

    @property
    def next_client_id(self):
        self.__next_client_id += 1
        return self.__next_client_id

    def set_loop(self, loop):
        self.__loop = loop

    def connect_from_client(self, conn: socket):
        connection = Connection(conn)
        client = ReClient(self.next_client_id, connection)
        self.__clients[conn.fileno()] = client

    def read_from_client(self, fd):
        client = self.__clients[fd]
        client.read_from_client()

    def write_to_client(self, fd):
        client = self.__clients[fd]
        client.write_to_client()

