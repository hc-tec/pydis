
from typing import Dict, List

from Client.interfaces import IClient
from Database.interfaces import IDatabase


class Database(IDatabase):

    def __init__(self, db_id):
        self._id = db_id
        self._dict = {}
        self._expires = {}
        self._blocking_keys = {}
        self._ready_keys = {}
        self._watch_keys: Dict[int, List[IClient]]  = {}

    def initial_with_dict(self, data_dict):
        init_fields = ['dict', 'expires', 'blocking_keys', 'ready_keys', '_watch_keys']
        for field in init_fields:
            setattr(self, field, data_dict.get(field, {}))

    def store(self, key, value):
        self._dict[key] = value

    def withdraw(self, key):
        return self._dict.get(key)

    def remove(self, key):
        if self.withdraw(key):
            del self._dict[key]

    def include(self, key) -> bool:
        return key in self._dict

    def store_expires(self, key, expires_time):
        self._expires[key] = expires_time

    def withdraw_expires(self, key):
        return self._expires.get(key)

    def remove_expires(self, key):
        if self.withdraw_expires(key):
            del self._expires[key]
        self.remove(key)

    def withdraw_watch_keys(self, key) -> List[IClient]:
        return self._watch_keys.get(key)

    def store_watch_keys(self, key, client_list: List[IClient]):
        self._watch_keys[key] = client_list

    def del_watch_key(self, key):
        del self._watch_keys[key]

    @property
    def __dict__(self):
        print(self._watch_keys)
        dict_data = {}
        accept_fields = ['id', 'dict', 'expires']
        for field in accept_fields:
            dict_data[field] = getattr(self, field)
        return dict_data

    def __str__(self):
        return '<{} id={}>'.format(
            self.__class__.__name__.lower(),
            self._id,
        )

    __repr__ = __str__

