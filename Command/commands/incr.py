
from Command.base import BaseCommand, CommandType


class Incr(BaseCommand):

    args_order = ['key']
    min_args = 1
    max_args = 1
    cmd_type = CommandType.CMD_WRITE

    def handle(self, args, kwargs):
        db = self.client.get_database()
        key = kwargs['key']
        value = db.withdraw(key)
        if value is None:
            db.store(key, 0)
            return 0
        else:
            db.store(key, value+1)
            return value+1
