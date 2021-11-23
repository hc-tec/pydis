
from Command.base import BaseCommand, CommandType
from Database.interfaces import IDatabase


class Get(BaseCommand):

    args_order = ['key']
    min_args = 1
    max_args = 1
    cmd_type = CommandType.CMD_READ

    def handle(self, args, kwargs):
        db: IDatabase = self.client.get_database()
        return db.withdraw(kwargs['key'])
