
from typing import Dict, Optional

from Generic.time import get_cur_time
from Sentinel.interfaces import ISentinelRedisInstance
from Sentinel.base import SRI_TYPE


class SentinelRedisInstance(ISentinelRedisInstance):

    def __init__(self, **kwargs):
        self._flag = None
        self._name = None
        self._run_id = kwargs['run_id']
        self._epoch = 0
        self._ip = kwargs['tcp_ip']
        self._port = kwargs['tcp_port']

        self._last_pub_time = get_cur_time()
        self._last_hello_time = get_cur_time()
        self._last_master_down_reply_time = get_cur_time()

        # Subjectively down since time
        self._s_down_since_time = None
        # Objectively down since time
        self._o_down_since_time = None
        self._down_after_period = None

        self._role_reported = kwargs['role']
        self._sentinels = {}
        self._slaves: Dict[str, ISentinelRedisInstance] = {}

        self._master: Optional[ISentinelRedisInstance] = None
        self._slave_master_host = None
        self._slave_master_port = 0

        self._leader = None
        self._leader_epoch = 0
        self._failover_epoch = 0
        self._failover_state = None
        self._failover_state_change_time = None
        self._failover_start_time = None
        self._failover_timeout = None

        self._info = kwargs['info']

    def modify(self, **kwargs):
        self._run_id = kwargs['run_id']
        self._ip = kwargs['tcp_ip']
        self._port = kwargs['tcp_port']
        self._role_reported = kwargs['role']
        self._info = kwargs['info']

    def get_info(self) -> dict:
        return self._info

    def set_master(self, master: ISentinelRedisInstance):
        self._master = master

    def get_master(self) -> ISentinelRedisInstance:
        return self._master

    def __str__(self):
        return '<{} run_id={}>'.format(
            self.__class__.__name__,
            self._run_id,
        )

    __repr__ = __str__
