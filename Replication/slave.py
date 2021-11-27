
from Client import Client
from Replication.base import REPL_SLAVE_STATE


class SLAVE_STATE:
    WAIT_BGSAVE_START = 0
    WAIT_BGSAVE_END = 1 << 0
    SEND_BULK = 1 << 1
    ONLINE = 1 << 2
