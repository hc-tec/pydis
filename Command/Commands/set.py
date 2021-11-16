
from Command import BaseCommand
from Database import Database
from Timer.event import TimeoutEvent
from Timer.timestamp import Timestamp
# from Server.server import server


class Set(BaseCommand):

    args_order = ['key', 'value', 'expires_time']
    min_args = 2

    def handle(self, args):
        db: Database = self.client.db
        expires_time = int(args.get('expires_time'))
        if expires_time is None:
            db.store(args['key'], args['value'])
        else:
            db.store(args['key'], args['value'])
            db.store_expires(args['key'], expires_time)
            self.set_expires_timer(args['key'], expires_time)

    def set_expires_timer(self, key, expires_time):
        timestamp = Timestamp(expires_time, 's')
        timeout_event = TimeoutEvent(timestamp)
        timeout_event.set_callback(Set.expires_event).set_extra_data({
            "client": self.client,
            "expires_key": key
        })
        server = self.client.get_server()
        reactor = server.get_loop()
        reactor.create_timeout_event(timeout_event)
        print('expire event build')

    @staticmethod
    def expires_event(reactor, extra_data):
        print('expire event activate')
        client = extra_data['client']
        db: Database = client.db
        print(db.expires, db.dict)
        db.remove_expires(extra_data['expires_key'])
        print(db.expires, db.dict)
