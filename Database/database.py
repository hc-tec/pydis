
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
    