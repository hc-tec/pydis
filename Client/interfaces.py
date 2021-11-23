
from socket import socket
from abc import ABCMeta, abstractmethod
from typing import Optional

from interfaces import IClosable
from Connection.interfaces import IConnection
from Command.interfaces import ICommand
from Database.interfaces import IDatabase

from Generic.patterns.observer import Observer
from IOLoop.interfaces import IReader, IWriter
from Pubsub.interfaces import IPubsubClientManager
from Replication.interfaces import IReplClientManager
from Server.interfaces import IServer
from Transaction.interfaces import ITransactionManager


class IClientHandler(metaclass=ABCMeta):

    @abstractmethod
    def data_received(self, data, client):
        ...

    @abstractmethod
    def command_executed_before(self, command: ICommand, client) -> bool:
        ...


class IClient(IClosable, Observer):

    flag = ''

    @abstractmethod
    def get_server(self) -> IServer:
        ...

    @abstractmethod
    def get_database(self) -> IDatabase:
        ...

    @abstractmethod
    def get_connection(self) -> IConnection:
        ...

    @abstractmethod
    def get_reader(self) -> IReader:
        ...

    @abstractmethod
    def get_writer(self) -> IWriter:
        ...

    @abstractmethod
    def get_handler(self) -> IClientHandler:
        ...

    @abstractmethod
    def get_repl_manager(self) -> IReplClientManager:
        ...

    @abstractmethod
    def get_transaction_manager(self) -> ITransactionManager:
        ...

    @abstractmethod
    def get_pubsub_manager(self) -> IPubsubClientManager:
        ...

    @abstractmethod
    def transform_handler(self, handler: IClientHandler):
        ...

    @abstractmethod
    def read_from_client(self):
        ...

    @abstractmethod
    def write_to_client(self) -> int:
        ...

    @abstractmethod
    def append_reply(self, reply):
        ...

    @abstractmethod
    def append_reply_enable_write(self, reply):
        ...

    @abstractmethod
    def handle_command(self, cmd_data):
        ...

    @abstractmethod
    def handle_command_after_resp(self, cmd_data):
        ...

    @abstractmethod
    def set_current_command(self, command: Optional[ICommand]) -> bool:
        ...

    @abstractmethod
    def touch_watched_key(self, command: ICommand):
        ...


class IResponse(metaclass=ABCMeta):

    @abstractmethod
    def append_reply(self, reply):
        ...


class IMasterHandler(IClientHandler):

    ...

    # @abstractmethod
    # def set_origin_cmd_sender(self, origin_cmd_sender):
    #     ...
    #
    # @abstractmethod
    # def get_origin_cmd_sender(self):
    #     ...
    #
    # @abstractmethod
    # def ping_ack(self, read_data, client):
    #     ...


class ISlaveHandler(IClientHandler):

    @abstractmethod
    def replicate(self, client: IClient):
        ...




