
from abc import ABCMeta, abstractmethod

from interfaces import IEnable


class IClusterNode(metaclass=ABCMeta):

    ...


class IClusterState(metaclass=ABCMeta):

    ...


class IClusterManager(IEnable):

    ...
