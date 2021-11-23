
from abc import ABCMeta, abstractmethod
from typing import List

from Client.interfaces import IClient


class IDatabase(metaclass=ABCMeta):

    @abstractmethod
    def initial_with_dict(self, data_dict):
        ...

    @abstractmethod
    def store(self, key, value):
        ...

    @abstractmethod
    def withdraw(self, key):
        ...

    @abstractmethod
    def remove(self, key):
        ...

    @abstractmethod
    def include(self, key) -> bool:
        ...

    @abstractmethod
    def store_expires(self, key, expires_time):
        ...

    @abstractmethod
    def withdraw_expires(self, key):
        ...

    @abstractmethod
    def remove_expires(self, key):
        ...

    @abstractmethod
    def withdraw_watch_keys(self, key) -> List[IClient]:
        ...

    @abstractmethod
    def store_watch_keys(self, key, client_list: List[IClient]):
        ...

    @abstractmethod
    def del_watch_key(self, key):
        ...


class IDatabaseManager(metaclass=ABCMeta):

    @abstractmethod
    def create_databases(self):
        ...

    @abstractmethod
    def get_database(self, index=0) -> IDatabase:
        ...

    @abstractmethod
    def get_databases(self) -> List[IDatabase]:
        ...

