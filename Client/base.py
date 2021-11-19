

class CLIENT_FLAG:
    SLAVE = 1 << 0
    MASTER = 1 << 1
    MONITOR = 1 << 2
    MULTI = 1 << 3
    BLOCKED = 1 << 4
    DIRTY_CAS = 1 << 5
    CLOSE_AFTER_REPLY = 1 << 6
    UNBLOCKED = 1 << 7
    LUA = 1 << 8
    ASKING = 1 << 9
    CLOSE_ASAP = 1 << 10
    UNIX_SOCKET = 1 << 11
    DIRTY_EXEC = 1 << 12
    MASTER_FORCE_REPLY = 1 << 13
    FORCE_AOF = 1 << 14
    FORCE_REPL = 1 << 15
    PRE_PSYNC = 1 << 16
    READONLY = 1 << 17
    PUBSUB = 1 << 18
    PREVENT_AOF_PROP = 1 << 19
    PREVENT_REPL_PROP = 1 << 20
    PREVENT_PROP = PREVENT_AOF_PROP | PREVENT_REPL_PROP
    PENDING_WRITE = 1 << 21
    REPLY_OFF = 1 << 22
    REPLY_SKIP_NEXT = 1 << 23
    REPLY_SKIP = 1 << 24
    LUA_DEBUG = 1 << 25
    LUA_DEBUG_SYNC = 1 << 26
    MODULE = 1 << 27
    PROTECTED = 1 << 28
    PENDING_COMMAND = 1 << 30
    ...

