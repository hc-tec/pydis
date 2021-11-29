

from Cluster.interfaces import IClusterState, IClusterManager
from Cluster.state import ClusterState


class ClusterManager(IClusterManager):

    def __init__(self):

        self._enable = None
        self._port = None
        self._timeout = None
        self._cluster: IClusterState = ClusterState()

        self._announce_ip = None
        self._announce_port = None
        self._announce_tls_port = None
        self._announce_bus_port = None

    def is_enable(self):
        return self._enable

    def enable(self):
        self._enable = True

    def disabled(self):
        self._enable = False









