

from Exception.base import BaseError


class DatabaseNotExistError(BaseError):
    msg = 'Database[{}] is not exist'

    def __init__(self, db_index):
        self.msg = self.msg.format(db_index)
