
from socket import socket


class IOWriter:

    @staticmethod
    def write_to_socket(sock: socket, data: str) -> int:
        if not sock and not data: return 0
        data = bytearray(data, "utf-8")
        send_len = 0
        try:
            while 1:
                send_len += sock.send(data[send_len:])
                if send_len == len(data):
                    break
        except (BrokenPipeError, ConnectionResetError) as e:
            print(e)
            return 0
        return 1
