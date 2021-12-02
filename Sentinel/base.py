

# Sentinel Redis Instance Type
class SRI_TYPE:
    MASTER = 1 << 0
    SLAVE = 1 << 1
    SENTINEL = 1 << 2
    S_DOWN = 1 << 3
    O_DOWN = 1 << 4
    MASTER_DOWN = 1 << 5
    FAILOVER_IN_PROGRESS = 1 << 6
    PROMOTED = 1 << 7
    RECONF_SENT = 1 << 8
    RECONF_INPROG = 1 << 9
    RECONF_DONE = 1 << 10
    FORCE_FAILOVER = 1 << 11
    SCRIPT_KILL_SENT = 1 << 12







