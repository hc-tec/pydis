
import socket

SOCK_READ_MAX = 1024


def socket_connect(host, addr):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, addr))
    sock.setblocking(False)
    return sock


def socket_read(sock: socket.socket, len_=SOCK_READ_MAX):
    return sock.recv(len_).decode('utf-8')


def socket_write(sock: socket.socket, data):
    data = bytearray(data, "utf-8")
    return sock.sendall(data)

