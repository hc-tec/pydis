
from abc import ABCMeta, abstractmethod
from typing import Tuple, List, Dict, Any, Set, Optional

from Generic.patterns.observer import Subject


class IChannel(metaclass=ABCMeta, Subject):

    @abstractmethod
    def set_subscribe_message(self):
        ...

    @abstractmethod
    def get_unsubscribe_message(self):
        ...

    @abstractmethod
    def set_publish_message(self, message):
        ...

    @abstractmethod
    def get_observers_num(self):
        ...


class IPubsubClientManager(metaclass=ABCMeta):

    @abstractmethod
    def get_pubsub_channels(self) -> Set:
        ...

    @abstractmethod
    def subscribe(self, channel):
        ...

    @abstractmethod
    def include(self, channel):
        ...

    @abstractmethod
    def remove(self, channel):
        ...


class IPubsubServerManager(metaclass=ABCMeta):

    @abstractmethod
    def get_channel(self, key) -> Optional[IChannel]:
        ...

    @abstractmethod
    def subscribe(self, key, channel: IChannel):
        ...

