class Database:

    def __init__(self, db_id):
        self.id = db_id
        self.dict = {}
        self.expires = {}
        self.blocking_keys = {}
        self.ready_keys = {}
        self.watch_keys = {}
    