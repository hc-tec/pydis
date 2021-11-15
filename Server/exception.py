

from Exception.base import BaseError


class BaseServerError(BaseError):
    msg = 'Server Error'


class DatabaseNotExistError(BaseServerError):
    msg = 'Database[{}] is not exist'

    def __init__(self, db_index):
        self.msg = self.msg.format(db_index)
