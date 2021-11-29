
from typing import List

from Generic.time import get_cur_time


class ClusterNode():

    def __init__(self):

        self._create_time = get_cur_time()
        self._name = ''
        self._flag = None
        self._num_slaves = 0
        self._slaves: List[ClusterNode] = []
        self._slaveof = None

        self._ping_sent = None
        self._pong_received = None
        self._data_received = None
        self._fail_time = None
        self._voted_time = None

        self._ip = None
        self._port = None

        self._link = None










