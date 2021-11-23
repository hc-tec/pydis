
from typing import List
from collections import deque

from Transaction.interfaces import ITransactionManager


class TransactionManager(ITransactionManager):

    def __init__(self):
        # multi
        self._buffer = deque()  # command queue
        self._watch_keys = []

    def get_buffer(self):
        return self._buffer

    def append_to_buffer(self, data):
        self._buffer.appendleft(data)

    def clear_buffer(self):
        self._buffer.clear()

    def get_watch_keys(self) -> List:
        return self._watch_keys

    def append_to_watch_key(self, data):
        self._watch_keys.append(data)

    def remove_from_watch_key(self, data):
        self._watch_keys.remove(data)
