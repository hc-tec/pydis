

from Generic.time import get_cur_time
from Sentinel.interfaces import ISentinelRedisInstance


class SentinelRedisInstance(ISentinelRedisInstance):

    def __init__(self):
        self._flag = None
        self._name = None
        self._run_id = None
        self._epoch = 0
        self._ip = None
        self._port = 0

        self._last_pub_time = get_cur_time()
        self._last_hello_time = get_cur_time()
        self._last_master_down_reply_time = get_cur_time()

        # Subjectively down since time
        self._s_down_since_time = None
        # Objectively down since time
        self._o_down_since_time = None
        self._down_after_period = None

        self._role_reported = None
        self._sentinels = {}
        self._slaves = {}

        self._slave_master_host = None
        self._slave_master_port = 0

        self._leader = None
        self._leader_epoch = 0
        self._failover_epoch = 0
        self._failover_state = None
        self._failover_state_change_time = None
        self._failover_start_time = None
        self._failover_timeout = None

        self._info = None

