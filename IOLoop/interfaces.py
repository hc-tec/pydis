
from abc import ABCMeta, abstractmethod

from Connection.interfaces import IConnection


class IReader(metaclass=ABCMeta):

    @abstractmethod
    def is_command_input_end(self) -> bool:
        ...

    @abstractmethod
    def clear_read_data(self):
        ...

    @abstractmethod
    def read_from_conn(self, conn: IConnection) -> str:
        ...


class IWriter(metaclass=ABCMeta):

    @abstractmethod
    def write_to_client(self, conn: IConnection) -> int:
        ...

    @abstractmethod
    def append_reply(self, reply):
        ...

    @abstractmethod
    def is_reply_empty(self):
        ...
