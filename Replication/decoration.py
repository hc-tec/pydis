
from Replication.base import REPL_SLAVE_STATE

def slave_check(func):
    def inner(cls):
        func(cls)
        if cls.read_data.startswith('REPLCONF listening-port'.lower()):
            cls.repl_state = REPL_SLAVE_STATE.RECEIVE_PORT
            cls.server.upgrade_client_to_master(cls)
    return inner

