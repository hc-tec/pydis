
from typing import Optional, List

from Client.interfaces import IClient
from Sentinel.interfaces import ISentinelManager


class SentinelManager(ISentinelManager):

    def __init__(self):
        self.message_connection: Optional[IClient] = None
        self.command_connection: Optional[IClient] = None
        self.message_conn_list: List[IClient] = []
        self.command_conn_list: List[IClient] = []

    def get_command_connection(self) -> List[IClient]:
        return self.command_conn_list

    def get_message_connection(self) -> List[IClient]:
        return self.message_conn_list

    def get_master_message_connection(self) -> IClient:
        return self.message_connection

    def set_message_connection(self, message_connection: IClient):
        self.message_connection = message_connection
        self.message_conn_list.append(message_connection)

    def get_master_command_connection(self) -> IClient:
        return self.command_connection

    def set_command_connection(self, command_connection: IClient):
        self.command_connection = command_connection
        self.command_conn_list.append(command_connection)

    def append_message_connection(self, message_connection: IClient):
        self.message_conn_list.append(message_connection)

    def append_command_connection(self, command_connection: IClient):
        self.command_conn_list.append(command_connection)

