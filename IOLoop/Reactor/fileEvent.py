
import errno
from socket import socket, error as sock_error

from IOLoop.Reactor.firedEvent import ReEvent
# from IOLoop.Reactor.Reactor import Reactor


class FileEvent:

    def __init__(self, client_sock: socket, client_addr):
        self.mask = ReEvent.RE_NONE
        self.client_sock = client_sock
        self.client_addr = client_addr
        self.clientData = None
