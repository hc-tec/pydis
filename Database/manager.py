
from typing import List

from Database.database import Database
from Database.interfaces import IDatabase, IDatabaseManager
from Database.exception import DatabaseNotExistError


class DatabaseManager(IDatabaseManager):

    def __init__(self):

        self.__databases: List[IDatabase] = []

        # Configuration
        self.db_num = 16

        self.create_databases()

    def create_databases(self):
        for i in range(self.db_num):
            self.__databases.append(Database(i))

    def get_database(self, index=0) -> IDatabase:
        # default database: db[0]
        if 0 <= index < self.db_num:
            return self.__databases[index]
        raise DatabaseNotExistError(index)

    def get_databases(self) -> List[IDatabase]:
        return self.__databases


