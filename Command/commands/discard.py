
from Client.interfaces import IClient
from Command.commands.unwatch import UnWatch
from Command.base import BaseCommand, CommandType
from Command.exception import DiscardWithoutMultiError
from Conf.command import CMD_RES
from Client.base import CLIENT_FLAG



class Discard(BaseCommand):

    args_order = []
    min_args = 0
    max_args = 0
    cmd_type = CommandType.CMD_COMMON

    def handle(self, args, kwargs):
        if self.client.flag & CLIENT_FLAG.MULTI:
            Discard.discard_transaction(self.client)
            return CMD_RES.OK
        else:
            raise DiscardWithoutMultiError()

    @staticmethod
    def discard_transaction(client: IClient):
        client.flag &= ~(CLIENT_FLAG.MULTI | CLIENT_FLAG.DIRTY_CAS | CLIENT_FLAG.DIRTY_EXEC)
        client.get_transaction_manager().clear_buffer()
        UnWatch.unwatched_all_keys(client)
