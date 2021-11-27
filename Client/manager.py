
from socket import socket
from typing import List, Dict

from Database.interfaces import IDatabase
from Connection.interfaces import IConnection
from Client.client import Client
from Client.interfaces import IClient
from Sentinel.handler import SentinelHandler
from Server.interfaces import IServer


class ClientManager():

    def __init__(self):

        self._next_client_id = 1
        self._clients: Dict[int, Client] = {}
        self._current_client = None

        # Limits
        self._max_clients = 1000

    @property
    def next_client_id(self):
        self._next_client_id += 1
        return self._next_client_id

    def connect_from_client(self, server: IServer, database: IDatabase, conn: socket) -> IClient:
        client = Client(server, self.next_client_id, database, conn)
        if server.is_sentinel_mode():
            client.transform_handler(SentinelHandler())
        self._clients[conn.fileno()] = client
        return client

    def read_from_client(self, fd) -> IConnection:
        client = self._clients[fd]
        client.read_from_client()
        return client.get_connection()

    def write_to_client(self, fd) -> IConnection:
        client = self._clients[fd]
        if client.write_to_client() == 0:
            del self._clients[fd]
        return client.get_connection()



