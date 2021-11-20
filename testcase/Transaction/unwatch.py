
import time
from Generic.socket import socket_connect, socket_read, socket_write

commands = [
    'set titto 456',
    'watch titto',
    'set titto 123',
    'unwatch',
    'multi',
    'get titto',
    'set titto 456',
    'get titto',
    'exec',
    'get titto'
]

sock = socket_connect('127.0.0.1', 9527)

for command in commands:
    socket_write(sock, f'{command}\n')
    time.sleep(0.5)
    print(socket_read(sock))
