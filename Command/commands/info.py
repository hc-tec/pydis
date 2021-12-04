
from Command.base import BaseCommand, CommandType
from Conf.command import CMD_RES


class Info(BaseCommand):
    need_kwargs = False
    cmd_type = CommandType.CMD_COMMON

    def handle(self, args, kwargs):
        return self.client.get_server().info()

    @staticmethod
    def parse_info(data: str) -> dict:
        res = {}
        info = data.split('\n')
        len_ = len(info)
        i = 0
        while i < len_:
            line = info[i]
            if not line:
                i += 1
                continue
            field, value = line.split(': ')
            res[field] = value
            if field == 'connected_slaves':
                value = int(value)
                if value:
                    slaves = set()
                    for host in info[i + 1:i + value + 1]:
                        ip, port = host.split()
                        slaves.add((ip, int(port)))
                    res['slaves_host'] = slaves
                    i += value
            i += 1
        return res
