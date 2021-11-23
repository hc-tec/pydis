
from abc import abstractmethod
from typing import List

from interfaces import IBufferManager


class ITransactionManager(IBufferManager):

    @abstractmethod
    def get_watch_keys(self) -> List:
        ...

    @abstractmethod
    def append_to_watch_key(self, data):
        ...

    @abstractmethod
    def remove_from_watch_key(self, data):
        ...
