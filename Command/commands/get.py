
from Command.base import BaseCommand, CommandType
from Database.database import Database


class Get(BaseCommand):

    args_order = ['key']
    min_args = 1
    max_args = 1
    cmd_type = CommandType.CMD_READ

    def handle(self, args, kwargs):
        db: Database = self.client.db
        return db.withdraw(kwargs['key'])
