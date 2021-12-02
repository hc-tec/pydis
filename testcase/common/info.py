
import time
from Generic.socket import socket_connect, socket_read, socket_write

commands = [
    'info'
]

sock = socket_connect('127.0.0.1', 9527)

for command in commands:
    socket_write(sock, f'{command}\n')
    time.sleep(0.5)
    print(socket_read(sock))
