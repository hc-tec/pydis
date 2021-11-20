
from Command.base import BaseCommand, CommandType
from Conf.command import CMD_RES
from Client.base import CLIENT_FLAG


class UnWatch(BaseCommand):

    need_kwargs = False
    cmd_type = CommandType.CMD_COMMON

    def handle(self, args, kwargs):
        UnWatch.unwatched_all_keys(self.client)
        self.client.flag &= ~CLIENT_FLAG.DIRTY_CAS
        self.client.flag &= ~CLIENT_FLAG.DIRTY_EXEC
        return CMD_RES.OK

    @staticmethod
    def unwatched_all_keys(client):
        for key, db in client.watch_keys:
            client.watch_keys.remove((key, db))

            watched_client_list = db.watch_keys[key]
            watched_client_list.remove(client)

            if not watched_client_list:
                del db.watch_keys[key]
