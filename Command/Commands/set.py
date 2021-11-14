
from Command import BaseCommand
from Database import Database


class Set(BaseCommand):

    args_order = ['key', 'value', 'expires_time']
    min_args = 2

    def handle(self, args):
        db: Database = self.client.db
        expires_time = args.get('expires_time')
        if expires_time is None:
            db.store(args['key'], args['value'])
        else:
            pass

