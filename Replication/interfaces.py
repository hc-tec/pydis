
from abc import ABCMeta, abstractmethod
from typing import List, Optional

from interfaces import ISyncAble
from Client.interfaces import IClient


class IReplState(metaclass=ABCMeta):

    @abstractmethod
    def get_repl_state(self) -> int:
        ...

    @abstractmethod
    def set_repl_state(self, repl_state):
        ...


class IReplClientManager(IReplState):

    @staticmethod
    def is_slave_connected(cls):
        ...

    @abstractmethod
    def get_repl_ack_time(self):
        ...

    @abstractmethod
    def update_repl_ack_time(self):
        ...

    @abstractmethod
    def set_addr_when_slave(self, host, port):
        ...


class IReplServerMasterManager(ISyncAble):

    @abstractmethod
    def select_slave(self) -> Optional[IClient]:
        ...

    @abstractmethod
    def get_slaves(self) -> List[IClient]:
        ...

    @abstractmethod
    def is_slave_connected(self, client: IClient) -> bool:
        ...

    @abstractmethod
    def get_connected_slaves(self) -> List[IClient]:
        ...

    @abstractmethod
    def append_slaves(self, slave: IClient):
        ...

    @abstractmethod
    def get_repl_ping_slave_period(self) -> int:
        ...


class IReplServerSlaveManager(IReplState):

    @abstractmethod
    def is_repl_slave_readonly(self) -> bool:
        ...

    @abstractmethod
    def get_master(self) -> IClient:
        ...

    @abstractmethod
    def set_master(self, master: IClient):
        ...

