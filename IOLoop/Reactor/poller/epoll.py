
import select

from .base import Poller
from IOLoop.Reactor.firedEvent import FiredEvent, ReEvent


class Epoll(Poller):

    def __init__(self):
        self.__create_epoll()

    def __create_epoll(self):
        self.__ep_fd = select.epoll()

    def register(self, fd, event):
        if event & ReEvent.RE_READABLE:
            self.__ep_fd.register(fd, select.EPOLLIN)
        elif event & ReEvent.RE_WRITABLE:
            self.__ep_fd.register(fd, select.EPOLLOUT)

    def unregister(self, fd):
        self.__ep_fd.unregister(fd)

    def modify(self, fd, event):
        if event & ReEvent.RE_READABLE:
            self.__ep_fd.modify(fd, select.EPOLLIN)
        elif event & ReEvent.RE_WRITABLE:
            self.__ep_fd.modify(fd, select.EPOLLOUT)

    def poll(self, reactor, timeout=None):
        # reactor.fired = {}
        events = self.__ep_fd.poll(timeout)
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
            reactor.fired[fd] = FiredEvent(fd, mask)
        return events
