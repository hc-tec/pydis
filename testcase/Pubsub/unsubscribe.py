
import time
from threading import Thread
from Generic.socket import socket_connect, socket_read, socket_write

class SubscribeTask(Thread):

    def run(self) -> None:
        commands = [
            'subscribe channel',
            'unsubscribe'
        ]
        sock = socket_connect('127.0.0.1', 9527)

        for command in commands:
            socket_write(sock, f'{command}\n')
            time.sleep(1)

        while True:
            try:
                print(socket_read(sock))
            except Exception:
                pass


class PublishTask(Thread):

    def run(self) -> None:
        commands = [
            'publish channel 123',
            'publish channel 456',
            'publish channel 780',
            'publish channel2 780',
            'publish channel3 780',
        ]
        sock = socket_connect('127.0.0.1', 9527)
        time.sleep(0.5)
        for command in commands:
            socket_write(sock, f'{command}\n')
            time.sleep(0.5)
            print(socket_read(sock))

subscribe = SubscribeTask()
publish = PublishTask()

subscribe.start()
publish.start()

subscribe.join()
publish.join()

