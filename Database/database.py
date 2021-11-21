
from Database.interfaces import IDatabase


class Database(IDatabase):

    def __init__(self, db_id):
        self.id = db_id
        self.dict = {}
        self.expires = {}
        self.blocking_keys = {}
        self.ready_keys = {}
        self.watch_keys = {}

    def initial_with_dict(self, data_dict):
        init_fields = ['dict', 'expires', 'blocking_keys', 'ready_keys', 'watch_keys']
        for field in init_fields:
            setattr(self, field, data_dict.get(field, {}))

    def store(self, key, value):
        self.dict[key] = value

    def withdraw(self, key):
        return self.dict.get(key)

    def remove(self, key):
        if self.withdraw(key):
            del self.dict[key]

    def store_expires(self, key, expires_time):
        self.expires[key] = expires_time

    def withdraw_expires(self, key):
        return self.expires.get(key)

    def remove_expires(self, key):
        if self.withdraw_expires(key):
            del self.expires[key]
        self.remove(key)

    @property
    def __dict__(self):
        print(self.watch_keys)
        dict_data = {}
        accept_fields = ['id', 'dict', 'expires']
        for field in accept_fields:
            dict_data[field] = getattr(self, field)
        return dict_data

    def __str__(self):
        return '<{} id={}>'.format(
            self.__class__.__name__.lower(),
            self.id,
        )

    __repr__ = __str__

