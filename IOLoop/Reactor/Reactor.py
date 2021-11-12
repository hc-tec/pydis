
import time
import socket

import select
import errno

from typing import Dict

from IOLoop.Reactor.poller.Epoll import Epoll
from IOLoop.Reactor.FiredEvent import FiredEvent
from IOLoop.Reactor.FileEvent import FileEvent
from IOLoop.Reactor.Acceptor import Acceptor


class Reactor:

    def __init__(self, ip, port):
        self.__acceptor = Acceptor(ip, port, self)
        self.poller = Epoll(self)

        self.ip = ip
        self.port = port
        self.fired: Dict[int, FiredEvent] = {}
        self.events: Dict[int, FileEvent] = {}

        self.poller.register(self.__acceptor.listen_fd(), select.EPOLLIN)

    # def clear_fired(self):
    #     self.fired = []

    def poll(self):
        events = self.poller.poll()
        if not events:
            return

        listen_fd = self.__acceptor.listen_fd()

        for fd, event in events:
            fired_event = self.fired[fd]

            if fd == listen_fd:
                self.__acceptor.accept()

            elif event & select.EPOLLIN:
                self.__acceptor.handle_read(fired_event)

            elif event & select.EPOLLOUT:
                self.__acceptor.handle_write(fired_event)

            elif event & select.EPOLLHUP:
                self.__acceptor.handle_close(fired_event)
