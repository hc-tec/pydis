
class Database:

    def __init__(self, db_id):
        self.id = db_id
        self.dict = {}
        self.expires = {}
        self.blocking_keys = {}
        self.ready_keys = {}
        self.watch_keys = {}

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

