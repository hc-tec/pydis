
import errno
from socket import socket, error as sock_error

from IOLoop.Reactor.firedEvent import ReEvent
# from IOLoop.Reactor.Reactor import Reactor


class FileEvent:

    def __init__(self, reactor, client_sock: socket, client_addr):
        self.reactor = reactor
        self.mask = ReEvent.RE_NONE
        self.client_sock = client_sock
        self.client_addr = client_addr
        self.clientData = None

    def read(self):
        data = ""
        while True:
            try:
                d = self.client_sock.recv(4096).decode("utf-8")
                if not d and not data:
                    return
                data += d
            except sock_error as e:
                if e.errno == errno.EAGAIN:
                    break
                else:
                    print(e)
                    return
            except UnicodeDecodeError as e:
                pass
        print(data)

    def write(self):
        data = "【Server】: Send\n"
        data = bytearray(data, "utf-8")
        sendlen = 0
        try:
            while 1:
                sendlen += self.client_sock.send(data[sendlen:])
                if sendlen == len(data):
                    break
        except BrokenPipeError as e:
            pass
