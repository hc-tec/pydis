
import select

from typing import Dict

from IOLoop.Reactor.poller import poller_class
from IOLoop.Reactor.firedEvent import FiredEvent, ReEvent
from IOLoop.Reactor.fileEvent import FileEvent
from IOLoop.Reactor.acceptor import Acceptor


class Reactor:

    def __init__(self, ip, port):
        self.__acceptor = Acceptor(ip, port, self)
        self.poller = poller_class()

        self.ip = ip
        self.port = port
        self.fired: Dict[int, FiredEvent] = {}
        self.events: Dict[int, FileEvent] = {}

        self.poller.register(self.__acceptor.listen_fd(), ReEvent.RE_READABLE)

    # def clear_fired(self):
    #     self.fired = []

    def poll(self):
        events = self.poller.poll(self, 10000)
        if not events:
            return

        listen_fd = self.__acceptor.listen_fd()

        for fd, event in events:
            fired_event = self.fired[fd]

            if fd == listen_fd:
                self.__acceptor.handle_accept()

            elif event & ReEvent.RE_READABLE:
                self.__acceptor.handle_read(fired_event)

            elif event & ReEvent.RE_WRITABLE:
                self.__acceptor.handle_write(fired_event)

            elif event & ReEvent.RE_CLOSE:
                self.__acceptor.handle_close(fired_event)
