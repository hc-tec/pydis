

from Connection.interfaces import IConnection
from IOLoop.Reactor.poller import poller_class
from IOLoop.Reactor.event import ReEvent
from IOLoop.Reactor.acceptor import Acceptor
from IOLoop.Reactor.interfaces import IReactor, IAcceptor, IAcceptorFactory
from IOLoop.Reactor.poller.interfaces import IPoller, IPollerFactory
from Timer.timer import Timer
from Timer.interfaces import ITimer, ITimerManager, ITimeoutEvent, ITimerFactory

MAX_TIMEOUT = 10


class TimerFactory(ITimerFactory):

    def build(self) -> ITimer:
        return Timer()


class PollerFactory(IPollerFactory):

    def build(self) -> IPoller:
        return poller_class()


class AcceptorFactory(IAcceptorFactory):

    def build(self, host: str, port: int):
        return Acceptor(host, port)


Default_Timer_Factory = TimerFactory()
Default_Poller_Factory = PollerFactory()
Default_Acceptor_Factory = AcceptorFactory()


class Reactor(IReactor, ITimerManager):

    def __init__(self,
                 host,
                 port,
                 acceptor_factory: IAcceptorFactory=Default_Acceptor_Factory,
                 timer_factory: ITimerFactory=Default_Timer_Factory,
                 poller_factory: IPollerFactory=Default_Poller_Factory):

        self.acceptor: IAcceptor = acceptor_factory.build(host, port)
        self.poller: IPoller = poller_factory.build()
        self.timer: ITimer = timer_factory.build()

        self.host = host
        self.port = port
        # self.events: Dict[int, FileEvent] = {}

        self.poller.register(self.acceptor.listen_fd(), ReEvent.RE_READABLE)

    # def clear_fired(self):
    #     self.fired = []
    def get_acceptor(self):
        return self.acceptor

    def get_poller(self):
        return self.poller

    def create_timeout_event(self, timeout_event: ITimeoutEvent):
        self.timer.add_event(timeout_event)

    def get_earliest_time(self):
        return self.timer.get_earliest_time()

    def process_timer_event(self):
        if self.timer.is_event_can_active():
            timeout_event = self.timer.pop_event()
            timeout_event.handle_event(self)

    def process_poll_event(self, events):
        listen_fd = self.acceptor.listen_fd()

        for fd, event in events:

            if fd == listen_fd:
                conn_fd = self.acceptor.connected()
                self.poller.register(conn_fd, ReEvent.RE_READABLE)

            elif event & ReEvent.RE_READABLE:
                conn: IConnection = self.acceptor.data_received(fd)
                conn_event = conn.get_event()
                if conn_event & ReEvent.RE_READABLE == 0:
                    self.poller.modify(fd, conn_event)

            elif event & ReEvent.RE_WRITABLE:
                conn: IConnection = self.acceptor.ready_to_write(fd)
                conn_event = conn.get_event()
                if conn_event & ReEvent.RE_WRITABLE == 0:
                    self.poller.modify(fd, conn_event)

            elif event & ReEvent.RE_CLOSE:
                self.acceptor.connect_close(fd)
                self.poller.unregister(fd)

    def poll(self):
        time = self.get_earliest_time() / 1000
        # print(time)
        events = self.poller.poll(min(time, MAX_TIMEOUT))

        self.process_poll_event(events)
        self.process_timer_event()
