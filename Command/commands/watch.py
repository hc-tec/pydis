
from typing import Optional, List
from Command.base import BaseCommand, CommandType
from Conf.command import CMD_RES
from Database.interfaces import IDatabase


class Watch(BaseCommand):

    need_kwargs = False
    cmd_type = CommandType.CMD_COMMON

    def handle(self, args, kwargs):
        client = self.client
        db: IDatabase = self.client.get_database()
        for key in args:
            if not db.include(key): continue
            client.get_transaction_manager().append_to_watch_key((key, db))
            watch_client_list: Optional[List] = db.withdraw_watch_keys(key)
            if watch_client_list:
                watch_client_list.append(client)
            else:
                db.store_watch_keys(key, [client])
        print(client)
        return CMD_RES.OK
