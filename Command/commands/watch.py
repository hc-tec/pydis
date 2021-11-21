
from typing import Optional, List
from Command.base import BaseCommand, CommandType
from Conf.command import CMD_RES
from Database.database import Database


class Watch(BaseCommand):

    need_kwargs = False
    cmd_type = CommandType.CMD_COMMON

    def handle(self, args, kwargs):
        client = self.client
        db: Database = self.client.db
        for key in args:
            if not key in db.dict: continue
            client.watch_keys.append((key, db))
            watch_client_list: Optional[List] = db.watch_keys.get(key)
            if watch_client_list:
                watch_client_list.append(client)
            else:
                db.watch_keys[key] = [client]
        print(client)
        return CMD_RES.OK
