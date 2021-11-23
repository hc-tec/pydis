
from Command.base import BaseCommand, CommandType
from Conf.command import CMD_RES
from Client.base import CLIENT_FLAG
from Client.interfaces import IClient
from Database.interfaces import IDatabase


class UnWatch(BaseCommand):

    need_kwargs = False
    cmd_type = CommandType.CMD_COMMON

    def handle(self, args, kwargs):
        UnWatch.unwatched_all_keys(self.client)
        self.client.flag &= ~CLIENT_FLAG.DIRTY_CAS
        self.client.flag &= ~CLIENT_FLAG.DIRTY_EXEC
        return CMD_RES.OK

    @staticmethod
    def unwatched_all_keys(client: IClient):
        transaction_manager = client.get_transaction_manager()
        for key, db in transaction_manager.get_watch_keys():
            db: IDatabase = db
            transaction_manager.remove_from_watch_key((key, db))

            watched_client_list = db.withdraw_watch_keys(key)
            watched_client_list.remove(client)

            if not watched_client_list:
                db.del_watch_key(key)
