

from Generic.patterns.observer import Observer, Subject
from Generic.decoration import alias


class Channels(Subject):

    @alias(Subject, 'attach')
    def subscribe(self, client):
        print(client)
        self._observers.append(client)


class Client(Observer):

    @alias(Observer, 'update')
    def receive(self, channel: Channels):
        print(channel, 1)

class Client2(Observer):

    def update(self, subject):
        print('sss')


channel = Channels()
client = Client()
client2 = Client2()
channel.attach(client)
channel.attach(client2)
channel.notify()

