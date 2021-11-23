
from typing import List, Set, Dict, Optional

from Pubsub.interfaces import IPubsubClientManager, IPubsubServerManager, IChannel


class PubsubClientManager(IPubsubClientManager):

    def __init__(self):

        self._pubsub_channels = set()
        self._pubsub_patterns = []

    def get_pubsub_channels(self) -> Set:
        return self._pubsub_channels

    def subscribe(self, channel):
        self._pubsub_channels.add(channel)

    def include(self, channel):
        return channel in self._pubsub_channels

    def remove(self, channel):
        self._pubsub_channels.remove(channel)


class PubsubServerManager(IPubsubServerManager):

    def __init__(self):
        # Pubsub
        self._pubsub_channels: Dict[str, IChannel] = {}
        self._pubsub_patterns = {}
        self._notify_keyspace_events = None

    def get_channel(self, key) -> Optional[IChannel]:
        return self._pubsub_channels.get(key)

    def subscribe(self, key, channel: IChannel):

        self._pubsub_channels[key] = channel
