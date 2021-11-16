
from Command.base import BaseCommand, CommandType
from Database import Database


class Get(BaseCommand):

    args_order = ['key']
    min_args = 1
    max_args = 1
    cmd_type = CommandType.CMD_READ

    def handle(self, args):
        db: Database = self.client.db
        return db.withdraw(args['key'])
