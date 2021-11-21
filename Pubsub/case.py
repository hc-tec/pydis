
from Pubsub.channel import Channel
from Pubsub.exception import ChannelIsNotExistError


class Pubsub:

    @staticmethod
    def subscribe(client, channel_name: str):
        client.pubsub_channels.add(channel_name)
        pubsub_channels: dict = client.server.pubsub_channels
        channel: Channel = pubsub_channels.get(channel_name)
        if not channel:
            channel = Channel(channel_name)
            pubsub_channels[channel_name] = channel
        channel.attach(client)
        channel.set_subscribe_message()
        channel.notify()

    @staticmethod
    def unsubscribe(client, channel_name: str):
        if not channel_name in client.pubsub_channels: return
        client.pubsub_channels.remove(channel_name)
        pubsub_channels: dict = client.server.pubsub_channels
        channel: Channel = pubsub_channels.get(channel_name)
        if not channel:
            return
        channel.detach(client)
        message = channel.get_unsubscribe_message()
        client.append_reply(message)
        # channel.notify()

    @staticmethod
    def unsubscribeAll(client):
        print(client.pubsub_channels)
        channels = [key for key in client.pubsub_channels]
        for channel_name in channels:
            Pubsub.unsubscribe(client, channel_name)

    @staticmethod
    def publish(client, channel_name: str, message: str) -> int:
        pubsub_channels: dict = client.server.pubsub_channels
        channel: Channel = pubsub_channels.get(channel_name)
        if not channel:
            raise ChannelIsNotExistError(channel_name)
        channel.set_publish_message(message)
        channel.notify()
        return channel.get_observers_num()
