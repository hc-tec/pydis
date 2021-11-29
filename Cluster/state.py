
from typing import Optional, List, Dict

from Cluster.interfaces import IClusterNode, IClusterState
from Cluster.node import ClusterNode


class ClusterState(IClusterState):

    def __init__(self):

        self._myself: Optional[IClusterNode] = None
        self._current_epoch = None
        self._state = None
        self._size = None
        self._nodes: Dict[str, IClusterNode] = {}
        self._nodes_black_list: Dict[str, IClusterNode] = {}











