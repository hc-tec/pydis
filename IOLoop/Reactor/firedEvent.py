

class ReEvent:
    RE_NONE = 0
    RE_READABLE = 1 << 0
    RE_WRITABLE = 1 << 1
    RE_BARRIER = 1 << 2
    RE_CLOSE = 1 << 3

class FiredEvent:

    def __init__(self, fd, mask):
        self.fd = fd
        self.mask = mask
