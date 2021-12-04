

from Client.handler import BaseHandler
from Client.interfaces import IClient
from Command.commands.info import Info
from Sentinel.interfaces import ISentinelManager


class SentinelHandler(BaseHandler):

    def data_received(self, data, client: IClient):
        if data.startswith('redis_version'):
            info = Info.parse_info(data)
            sentinel_manager: ISentinelManager = client.get_server().get_sentinel_manager()
            sentinel_manager.build_redis_instance(client, info)
            print(info)
        client.get_connection().enable_write()
        client.get_reader().clear_read_data()













