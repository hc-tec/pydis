
import select
from IOLoop.Reactor import Reactor
from IOLoop.Reactor.FiredEvent import FiredEvent, ReEvent


class Epoll:

    def __init__(self, reactor: Reactor):
        self.__reactor = reactor
        self.__create_epoll()

    def __create_epoll(self):
        self.__ep_fd = select.epoll()

    def register(self, fd, event):
        self.__ep_fd.register(fd, event)

    def unregister(self, fd):
        self.__ep_fd.unregister(fd)

    def modify(self, fd, event):
        self.__ep_fd.modify(fd, event)

    def poll(self):
        self.__reactor.fired = {}
        events = self.__ep_fd.poll()
        mask = 0
        for fd, event in events:
            if event & select.EPOLLIN:
                mask |= ReEvent.RE_READABLE
            elif event & select.EPOLLOUT:
                mask |= ReEvent.RE_WRITABLE
            elif event & select.EPOLLERR:
                mask |= ReEvent.RE_READABLE | ReEvent.RE_WRITABLE
            elif event & select.EPOLLHUP:
                mask |= ReEvent.RE_READABLE | ReEvent.RE_WRITABLE
            self.__reactor.fired[fd] = FiredEvent(fd, mask)
        return events
