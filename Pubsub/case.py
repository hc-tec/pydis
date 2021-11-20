
from Pubsub.channel import Channel
from Pubsub.exception import ChannelIsNotExistError


class Pubsub:

    @staticmethod
    def subscribe(client, channel_name: str):
        client.pubsub_channels[channel_name] = None
        pubsub_channels: dict = client.server.pubsub_channels
        channel: Channel = pubsub_channels.get(channel_name)
        if not channel:
            channel = Channel(channel_name)
            pubsub_channels[channel_name] = channel
        channel.attach(client)
        channel.notify()

    @staticmethod
    def publish(client, channel_name: str, message: str) -> int:
        pubsub_channels: dict = client.server.pubsub_channels
        channel: Channel = pubsub_channels.get(channel_name)
        if not channel:
            raise ChannelIsNotExistError(channel_name)
        channel.set_message(message)
        channel.notify()
        return channel.get_observers_num()
