

import select

from IOLoop.Reactor.interfaces import IPoller
from IOLoop.Reactor.event import ReEvent


class Select(IPoller):

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

    def clear_broken_fd(self):
        try:
            self.__writers.remove(-1)
        except KeyError:
            pass
        try:
            self.__readers.remove(-1)
        except KeyError:
            pass

    def poll(self, timeout=None):
        ready = []
        timeout = max(timeout, 0)
        try:
            r, w, x = select.select(self.__readers, self.__writers, [], timeout)
        except InterruptedError:
            return ready
        except ValueError:
            self.clear_broken_fd()
            r, w, x = select.select(self.__readers, self.__writers, [], timeout)
        r = set(r)
        w = set(w)
        for fd in r | w:
            mask = ReEvent.RE_NONE
            if fd in r:
                mask |= ReEvent.RE_READABLE
            if fd in w:
                mask |= ReEvent.RE_WRITABLE
            ready.append((fd, mask))
        return ready


