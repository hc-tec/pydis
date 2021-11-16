
from typing import Dict, List

from socket import socket
from Client import Client
from Connection import Connection
from Database import Database
from Server.exception import DatabaseNotExistError


class Server:

    def __init__(self):
        self.__next_client_id = 1
        self.__loop = None
        self.__clients: Dict[int, Client] = {}
        self.__slaves = []
        self.__monitors = []
        self.__current_client = None
        self.__databases: List[Database] = []

        # RDB / AOF
        self.loading = False

        # Configuration
        self.db_num = 16

        # Limits
        self.max_clients = 1000

        self.create_databases()

    def create_databases(self):
        for i in range(self.db_num):
            self.__databases.append(Database(i))

    def get_database(self, index=0) -> Database:
        # default database: db[0]
        if 0 <= index < self.db_num:
            return self.__databases[index]
        raise DatabaseNotExistError(index)

    @property
    def next_client_id(self):
        self.__next_client_id += 1
        return self.__next_client_id

    def set_loop(self, loop):
        self.__loop = loop

    def get_loop(self):
        return self.__loop

    def connect_from_client(self, conn: socket):
        connection = Connection(conn, self.__loop)
        client = Client(self, self.next_client_id, self.get_database(), connection)
        self.__clients[conn.fileno()] = client

    def read_from_client(self, fd):
        client = self.__clients[fd]
        client.read_from_client()

    def write_to_client(self, fd):
        client = self.__clients[fd]
        client.write_to_client()

server = Server()
