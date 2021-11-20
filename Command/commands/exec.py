
from Conf.command import CMD_RES
from Client.base import CLIENT_FLAG
from Command.commands.discard import Discard

from Command.base import BaseCommand, CommandType
from Command.exception import ExecWithoutMultiError
from Exception.base import BaseError


class Exec(BaseCommand):

    args_order = []
    min_args = 0
    max_args = 0
    cmd_type = CommandType.CMD_COMMON

    def handle(self, args, kwargs):
        if not (self.client.flag & CLIENT_FLAG.MULTI):
            raise ExecWithoutMultiError()
        if self.is_watched_key_expired():
            self.client |= CLIENT_FLAG.DIRTY_CAS
        # when watched keys changed, discard the transaction
        if self.client.flag & (CLIENT_FLAG.DIRTY_CAS | CLIENT_FLAG.DIRTY_EXEC):
            Discard.discard_transaction(self.client)
            return

        commands = self.client.ms_state
        results = self.execute_all_commands(commands)

        self.client.flag &= ~CLIENT_FLAG.MULTI
        return results

    def execute_all_commands(self, commands):
        results = ''
        index = 1
        while len(commands):
            command, args = commands.pop()
            try:
                result = command.execute(args)
            except BaseError as e:
                Discard.discard_transaction(self.client)
                raise e
            if result:
                results += f'{index}) {result}\n'
            else:
                results += '(nil)\n'
            index += 1
        return results

    def is_watched_key_expired(self) -> bool:
        client = self.client
        for key, db in client.watch_keys:
            if not key in db.dict:
                return True
        return False


