
from Client.interfaces import IClient
from Pubsub.channel import Channel
from Pubsub.exception import ChannelIsNotExistError


class Pubsub:

    @staticmethod
    def subscribe(client: IClient, channel_name: str):
        client.get_pubsub_manager().subscribe(channel_name)
        pubsub_server_manager = client.get_server().get_pubsub_manager()
        channel = pubsub_server_manager.get_channel(channel_name)
        if not channel:
            channel = Channel(channel_name)
            pubsub_server_manager.subscribe(channel_name, channel)
        channel.attach(client)
        channel.set_subscribe_message()
        channel.notify()

    @staticmethod
    def unsubscribe(client: IClient, channel_name: str):
        pubsub_manager = client.get_pubsub_manager().include(channel_name)
        if not pubsub_manager: return
        pubsub_manager.remove(channel_name)
        pubsub_server_manager = client.get_server().get_pubsub_manager()
        channel = pubsub_server_manager.get_channel(channel_name)
        if not channel:
            return
        channel.detach(client)
        message = channel.get_unsubscribe_message()
        client.append_reply(message)
        # channel.notify()

    @staticmethod
    def unsubscribeAll(client: IClient):
        channels = [key for key in client.get_pubsub_manager().get_pubsub_channels()]
        for channel_name in channels:
            Pubsub.unsubscribe(client, channel_name)

    @staticmethod
    def publish(client: IClient, channel_name: str, message: str) -> int:
        pubsub_server_manager = client.get_server().get_pubsub_manager()
        channel = pubsub_server_manager.get_channel(channel_name)
        if not channel:
            raise ChannelIsNotExistError(channel_name)
        channel.set_publish_message(message)
        channel.notify()
        return channel.get_observers_num()
