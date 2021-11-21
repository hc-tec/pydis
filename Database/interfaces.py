
from abc import ABCMeta, abstractmethod


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
    def store_expires(self, key, expires_time):
        ...

    @abstractmethod
    def withdraw_expires(self, key):
        ...

    @abstractmethod
    def remove_expires(self, key):
        ...


class IDatabaseManager(metaclass=ABCMeta):

    @abstractmethod
    def create_databases(self):
        ...

    @abstractmethod
    def get_database(self, index=0) -> IDatabase:
        ...

    @abstractmethod
    def get_databases(self):
        ...


class IPersistence(metaclass=ABCMeta):

    @abstractmethod
    def save(self, server):
        pass

    @abstractmethod
    def load(self, server):
        pass


class IPersistenceManager(metaclass=ABCMeta):

    @abstractmethod
    def load_persistent_file(self):
        ...

    @abstractmethod
    def load_from_master(self, data):
        ...


class IRDBCaller(metaclass=ABCMeta):

    @abstractmethod
    def rdb_start(self):
        ...

    @abstractmethod
    def rdb_reset(self):
        ...
