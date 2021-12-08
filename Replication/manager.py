
from typing import List, Optional

from interfaces import ISyncAble
from Client.interfaces import IClient
from Replication.base import REPL_SLAVE_STATE
from Generic.time import get_cur_time
from Replication.interfaces import IReplClientManager, IReplServerMasterManager, IReplServerSlaveManager
from Generic.utils import generate_uuid


class ReplClientManager(IReplClientManager):

    def __init__(self):

        # Replication
        self._repl_id = None
        self._repl_state = REPL_SLAVE_STATE.NONE
        self._repl_ack_time = None
        # (host, port), used in master keepalive system
        self._host_as_slave = None
        self._port_as_slave = None

    def get_repl_id(self) -> str:
        return self._repl_id

    def set_repl_id(self, repl_id: str):
        self._repl_id = repl_id

    @staticmethod
    def is_slave_connected(cls: IReplClientManager):
        return cls.get_repl_state() == REPL_SLAVE_STATE.CONNECTED

    def get_repl_state(self) -> int:
        return self._repl_state

    def set_repl_state(self, repl_state):
        self._repl_state = repl_state

    def get_repl_ack_time(self):
        return self._repl_ack_time

    def update_repl_ack_time(self):
        self._repl_ack_time = get_cur_time()

    def set_addr_when_slave(self, host, port):
        self._host_as_slave = host
        self._port_as_slave = port

    def get_host_when_slave(self) -> str:
        return f'{self._host_as_slave} {self._port_as_slave}'


class ReplServerMasterManager(IReplServerMasterManager):

    def __init__(self):
        # Replication (master)
        self._repl_id = generate_uuid()
        self._repl_ping_slave_period = 10  # Master pings the slave every N seconds
        self._repl_good_slaves_count = 0
        self._repl_min_slaves_to_write = 0
        self._repl_min_slaves_max_lag = 10
        self._repl_slaves: List[IClient] = []
        self._need_sync = False
        self._repl_slaves_rb_num = -1

    def get_repl_ping_slave_period(self) -> int:
        return self._repl_ping_slave_period

    def append_slaves(self, slave: IClient):
        self._repl_slaves.append(slave)

    def is_slave_connected(self, client: IClient) -> bool:
        return ReplClientManager.is_slave_connected(client.get_repl_manager())

    def get_slaves_num(self) -> int:
        return len(self._repl_slaves)

    def get_slaves_host(self) -> str:
        res = ''
        for slave in self._repl_slaves:
            res += slave.get_repl_manager().get_host_when_slave() + '\n'
        return res

    def get_slaves(self) -> List[IClient]:
        return self._repl_slaves

    def select_slave(self) -> Optional[IClient]:
        if self._repl_slaves:
            usable_slaves = list(filter(self.is_slave_connected, self._repl_slaves))
            self._repl_slaves_rb_num = (self._repl_slaves_rb_num+1) % len(usable_slaves)
            return usable_slaves[self._repl_slaves_rb_num]
        return None

    def get_connected_slaves(self) -> List[IClient]:
        return list(filter(self.is_slave_connected, self._repl_slaves))

    def need_sync(self):
        return self._need_sync

    def sync_enable(self):
        self._need_sync = True

    def sync_disable(self):
        self._need_sync = False


class ReplServerSlaveManager(IReplServerSlaveManager):

    def __init__(self):

        # Replication (slave)
        self._master_host = None
        self._master_port = None
        self._master = None
        self._repl_state = REPL_SLAVE_STATE.NONE
        self._repl_slave_ro = True

    def is_repl_slave_readonly(self) -> bool:
        return self._repl_slave_ro

    def get_repl_state(self) -> int:
        return self._repl_state

    def set_repl_state(self, repl_state):
        self._repl_state = repl_state

    def get_master(self) -> IClient:
        return self._master

    def set_master(self, master: IClient):
        self._master = master

    def set_addr(self, host, port):
        self._master_host = host
        self._master_port = port

