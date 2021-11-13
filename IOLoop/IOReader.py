
import errno
from socket import socket, error as sock_error

MAX_READ_ONCE = 1024


class IOReader:

    @staticmethod
    def read_from_socket(sock: socket):
        if not sock:
            return ''
        data = ''
        while True:
            try:
                d = sock.recv(MAX_READ_ONCE).decode("utf-8")
                if not d and not data:
                    return ''
                data += d
            except sock_error as e:
                if e.errno == errno.EAGAIN:
                    break
                else:
                    print(e)
                    return ''
            except UnicodeDecodeError as e:
                pass
        print(data)
        return data
