
from typing import List, Tuple

from Command.commands import COMMAND_DICT
from Command.base import BaseCommand, CommandNotExist
from Exception.base import BaseError

from Client.base import CLIENT_FLAG


class CommandHandler:

    def __init__(self, client, cmd_data):
        self.client = client
        self.cmd_name = ''
        self.raw_cmd = cmd_data
        self.cmd_data = cmd_data.split()

    def is_cmd_exist(self):
        return COMMAND_DICT.get(self.cmd_name)

    def handle(self):
        try:
            command, args = self.parse_command()
            is_continue = self.client.set_current_command(command)
            if is_continue:
                # when enter multi env
                # push command to the command queue
                if self.client.flag & CLIENT_FLAG.MULTI:
                    self.client.ms_state.appendleft((command, args))
                    self.client.append_reply('QUEUED\n')
                else:
                    result = command.execute(args)
                    if result:
                        self.client.append_reply(f'{result}\n')

        except BaseError as e:
            self.client.append_reply(e.msg)
        finally:
            self.client.set_current_command(None)

    def parse_command(self) -> Tuple[BaseCommand, List]:
        try:
            self.cmd_name = self.cmd_data[0]
        except IndexError:
            pass
        command = self.is_cmd_exist()
        if command:
            return command(self.client, self.raw_cmd), self.cmd_data[1:]
        raise CommandNotExist()
