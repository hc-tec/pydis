
from socket import socket
from abc import ABCMeta, abstractmethod

from Client.interfaces import IClient
from Database.interfaces import IDatabaseManager
from Database.persistence.interfaces import IPersistenceManager, IRDBManager, IAOFManager
from Pubsub.interfaces import IPubsubServerManager
from Replication.interfaces import IReplServerSlaveManager, IReplServerMasterManager
from IOLoop.Reactor.interfaces import IReactor


class IServer(metaclass=ABCMeta):

    @abstractmethod
    def get_loop(self) -> IReactor:
        ...

    @abstractmethod
    def set_loop(self, loop: IReactor):
        ...

    @abstractmethod
    def incr_watchdog_run_num(self):
        ...

    @abstractmethod
    def start_watchdog(self):
        ...

    @abstractmethod
    def set_addr(self, host, port):
        ...

    @abstractmethod
    def get_addr(self) -> dict:
        ...

    @abstractmethod
    def get_database_manager(self) -> IDatabaseManager:
        ...

    @abstractmethod
    def get_persistence_manager(self) -> IPersistenceManager:
        ...

    @abstractmethod
    def get_rdb_manager(self) -> IRDBManager:
        ...

    @abstractmethod
    def get_aof_manager(self) -> IAOFManager:
        ...

    @abstractmethod
    def get_repl_master_manager(self) -> IReplServerMasterManager:
        ...

    @abstractmethod
    def get_repl_slave_manager(self) -> IReplServerSlaveManager:
        ...

    @abstractmethod
    def get_pubsub_manager(self) -> IPubsubServerManager:
        ...

    @abstractmethod
    def load_persistence_file(self):
        ...

    @abstractmethod
    def start_aof(self):
        ...

    @abstractmethod
    def start_rdb(self):
        ...

    @abstractmethod
    def write_cmd_increment(self):
        ...

    @abstractmethod
    def connect_from_client(self, conn: socket) -> IClient:
        ...

    @abstractmethod
    def connect_to_master(self, conn: socket, slaveof_cmd_sender: IClient):
        ...

    @abstractmethod
    def read_from_client(self, fd):
        ...

    @abstractmethod
    def write_to_client(self, fd):
        ...

    @abstractmethod
    def upgrade_client_to_master(self, client: IClient):
        ...

    @abstractmethod
    def EVETY_SECOND(self, second=1):
        ...

