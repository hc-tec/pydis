
from Command.base import BaseCommand, CommandType
from Conf.command import CMD_RES
from Client.base import CLIENT_FLAG


class Exec(BaseCommand):

    args_order = []
    min_args = 0
    max_args = 0
    cmd_type = CommandType.CMD_COMMON

    def handle(self, args, kwargs):
        commands = self.client.ms_state
        results = []
        index = 1
        while len(commands):
            command, args = commands.pop()
            result = command.execute(args)
            if result:
                results.append(f'{index}) {result}\n')
            else:
                results.append('(nil)\n')
            index += 1
        self.client.flag &= ~CLIENT_FLAG.MULTI
        return results
