
from Command.base import BaseCommand, CommandType
from Database.database import Database
from Timer.event import TimeoutEvent
from Timer.timestamp import Timestamp
from Conf.command import CMD_RES


class Set(BaseCommand):

    args_order = ['key', 'value', 'expires_time']
    min_args = 2
    cmd_type = CommandType.CMD_WRITE

    def handle(self, args, kwargs):
        db: Database = self.client.db
        expires_time = kwargs.get('expires_time')
        if expires_time is None:
            db.store(kwargs['key'], kwargs['value'])
        else:
            expires_time = int(expires_time)
            db.store(kwargs['key'], kwargs['value'])
            self.set_expires_timer(kwargs['key'], expires_time)
        return CMD_RES.OK

    def set_expires_timer(self, key, expires_time):
        db: Database = self.client.db
        timestamp = Timestamp(expires_time, 's')
        db.store_expires(key, timestamp.get_time())
        timeout_event = ExpiresKeyRemoveEvent(timestamp)
        timeout_event.set_extra_data({
            "client": self.client,
            "expires_key": key
        })
        server = self.client.get_server()
        reactor = server.get_loop()
        reactor.create_timeout_event(timeout_event)
        print('expire event build')


class ExpiresKeyRemoveEvent(TimeoutEvent):

    def handle_event(self, reactor):
        extra_data = self.extra_data
        print('expire event activate')
        client = extra_data['client']
        db: Database = client.db
        print(db.expires, db.dict)
        db.remove_expires(extra_data['expires_key'])
        print(db.expires, db.dict)
