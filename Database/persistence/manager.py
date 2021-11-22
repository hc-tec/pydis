
from Database.persistence.base import PERS_STATUS
from Database.persistence.AOF import AOFManager
from Database.persistence.RDB import RDBManager
from Database.persistence.interfaces import IPersistenceManager


class PersistenceManager(IPersistenceManager):

    def __init__(self):
        # persistence status
        self._pers_status = PERS_STATUS.NO_WRITE

        self._aof_manager = AOFManager()
        self._rdb_manager = RDBManager()

    def get_pers_status(self):
        return self._pers_status

    def set_pers_status(self, status):
        self._pers_status = status

    def get_aof_manager(self):
        return self._aof_manager

    def get_rdb_manager(self):
        return self._rdb_manager

