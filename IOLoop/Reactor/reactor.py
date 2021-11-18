

from typing import Dict

from IOLoop.Reactor.poller import poller_class
from IOLoop.Reactor.firedEvent import FiredEvent, ReEvent
from IOLoop.Reactor.fileEvent import FileEvent
from IOLoop.Reactor.acceptor import Acceptor
from Timer.timer import Timer
from Timer.event import TimeoutEvent


MAX_TIMEOUT = 10


class Reactor:

    def __init__(self, host, port):
        self.__acceptor = Acceptor(host, port)
        self.poller = poller_class()
        self.timer = Timer()

        self.host = host
        self.port = port
        self.fired: Dict[int, FiredEvent] = {}
        self.events: Dict[int, FileEvent] = {}

        self.poller.register(self.__acceptor.listen_fd(), ReEvent.RE_READABLE)

    # def clear_fired(self):
    #     self.fired = []
    def get_acceptor(self):
        return self.__acceptor

    def get_poller(self):
        return self.poller

    def create_timeout_event(self, timeout_event: TimeoutEvent):
        self.timer.add_event(timeout_event)

    def get_earliest_time(self):
        return self.timer.get_earliest_time()

    def process_timer_event(self):
        if self.timer.is_event_can_active():
            timeout_event = self.timer.pop_event()
            timeout_event.handle_event(self)

    def process_poll_event(self, events):
        listen_fd = self.__acceptor.listen_fd()

        for fd, event in events:
            fired_event = self.fired[fd]

            if fd == listen_fd:
                self.__acceptor.handle_accept(self.events, self.poller)

            elif event & ReEvent.RE_READABLE:
                self.__acceptor.handle_read(fired_event)

            elif event & ReEvent.RE_WRITABLE:
                self.__acceptor.handle_write(fired_event)

            elif event & ReEvent.RE_CLOSE:
                self.__acceptor.handle_close(self.poller, fired_event)

    def poll(self):
        time = self.get_earliest_time() / 1000
        # print(time)
        events = self.poller.poll(self, min(time, MAX_TIMEOUT))

        self.process_poll_event(events)
        self.process_timer_event()
