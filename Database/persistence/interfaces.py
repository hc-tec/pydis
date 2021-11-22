
from abc import ABCMeta, abstractmethod

from interfaces import IEnable, IBufferManager
from Database.interfaces import IDatabaseManager


class IPersistenceManager(metaclass=ABCMeta):

    @abstractmethod
    def get_aof_manager(self):
        ...

    @abstractmethod
    def get_rdb_manager(self):
        ...

    @abstractmethod
    def get_pers_status(self):
        ...

    @abstractmethod
    def set_pers_status(self, status):
        ...


class IPersistenceMethod(metaclass=ABCMeta):

    def __init__(self, file_path):
        self._save_file_path = file_path

    def get_save_file_path(self):
        return self._save_file_path

    @abstractmethod
    def save(self, *args, **kwargs):
        pass

    @abstractmethod
    def load(self, *args, **kwargs):
        pass


class IRDB(IPersistenceMethod):

    def load_from_data(self, server, data):
        ...


class IPersistenceMethodManager(IEnable):

    @abstractmethod
    def reset(self):
        ...

    @abstractmethod
    def start(self, *args, **kwargs):
        ...

    @abstractmethod
    def load_file(self, db_manager: IDatabaseManager):
        ...


class IAOFManager(IPersistenceMethodManager, IBufferManager):

    @abstractmethod
    def get_rewrite_last_time(self):
        ...

    @abstractmethod
    def reset_rewrite_time(self):
        ...


class IRDBManager(IPersistenceMethodManager):

    @abstractmethod
    def get_dirty(self):
        ...

    @abstractmethod
    def incr_dirty(self):
        ...

    @abstractmethod
    def get_dirty_before_bgsave(self):
        ...

    @abstractmethod
    def get_save_params(self):
        ...

    @abstractmethod
    def reset(self):
        ...

    @abstractmethod
    def load_from_master(self, db_manager: IDatabaseManager, data):
        ...

