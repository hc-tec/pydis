
from abc import ABCMeta, abstractmethod
from typing import List

from Client.interfaces import IClient


class ISentinelManager(metaclass=ABCMeta):

    @abstractmethod
    def get_master_message_connection(self) -> IClient:
        ...

    @abstractmethod
    def get_message_connection(self) -> List[IClient]:
        ...

    @abstractmethod
    def set_message_connection(self, message_connection: IClient):
        ...

    @abstractmethod
    def get_master_command_connection(self) -> IClient:
        ...

    @abstractmethod
    def get_command_connection(self) -> List[IClient]:
        ...

    @abstractmethod
    def set_command_connection(self, command_connection: IClient):
        ...

    @abstractmethod
    def append_message_connection(self, message_connection: IClient):
        ...

    @abstractmethod
    def append_command_connection(self, message_connection: IClient):
        ...







