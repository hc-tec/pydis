

import select

from .base import Poller
from IOLoop.Reactor.firedEvent import ReEvent, FiredEvent

class Select(Poller):

    def __init__(self):
        self.__readers = set()
        self.__writers = set()

    def register(self, fd, event):
        if event & ReEvent.RE_READABLE:
            self.__readers.add(fd)
        elif event & ReEvent.RE_WRITABLE:
            self.__writers.add(fd)

    def unregister(self, fd):
        self.__readers.discard(fd)
        self.__writers.discard(fd)

    def modify(self, fd, event):
        self.unregister(fd)
        self.register(fd, event)

    def poll(self, reactor, timeout=None):
        ready = []
        try:
            r, w, x = select.select(self.__readers, self.__writers, [], timeout)
        except InterruptedError:
            return ready
        r = set(r)
        w = set(w)
        for fd in r | w:
            mask = 0
            if fd in r:
                mask |= ReEvent.RE_READABLE
            if fd in w:
                mask |= ReEvent.RE_WRITABLE
            ready.append((fd, mask))
            reactor.fired[fd] = FiredEvent(fd, mask)
        return ready


