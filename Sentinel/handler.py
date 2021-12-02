

from Client.handler import BaseHandler
from Client.interfaces import IClient
from Sentinel.interfaces import ISentinelManager


class SentinelHandler(BaseHandler):

    def data_received(self, data, client: IClient):
        if data.startswith('redis_version'):
            info = self.parse_info(data)
            sentinel_manager: ISentinelManager = client.get_server().get_sentinel_manager()
            sentinel_manager.build_redis_instance(client.get_server(), info)
            print(info)
        client.get_connection().enable_write()
        client.get_reader().clear_read_data()

    def parse_info(self, data: str):
        res = {}
        info = data.split('\n')
        len_ = len(info)
        i = 0
        while i < len_:
            line = info[i]
            if not line:
                i += 1
                continue
            print(line)
            field, value = line.split(': ')
            res[field] = value
            if field == 'connected_slaves':
                value = int(value)
                if value:
                    slaves = set()
                    for host in info[i+1:i+value+1]:
                        ip, port = host.split()
                        slaves.add((ip, int(port)))
                    res['slaves_host'] = slaves
                    i += value
            i += 1
        return res











