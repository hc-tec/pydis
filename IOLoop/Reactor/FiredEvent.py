
from enum import Enum


class ReEvent:
    RE_NONE = 0
    RE_READABLE = 1
    RE_WRITABLE = 2
    RE_BARRIER = 4


class FiredEvent:

    def __init__(self, fd, mask):
        self.fd = fd
        self.mask = mask
