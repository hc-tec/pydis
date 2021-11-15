
from typing import List, Tuple

from .Commands import COMMAND_DICT
from .base import BaseCommandError, BaseCommand, CommandNotExist


class CommandHandler:

    def __init__(self, client, cmd_data):
        self.client = client
        self.cmd_name = ''
        self.cmd_data = cmd_data.split()

    def is_cmd_exist(self):
        return COMMAND_DICT.get(self.cmd_name)

    def handle(self):
        try:
            command, args = self.parse_command()
            result = command.execute(args)
            if result:
                self.client.append_reply(result)
            else:
                self.client.append_reply('(ok) \n')
        except BaseCommandError as e:
            self.client.append_reply(e.msg)

    def parse_command(self) -> Tuple[BaseCommand, List]:
        try:
            self.cmd_name = self.cmd_data[0]
        except IndexError:
            pass
        command = self.is_cmd_exist()
        if command:
            return command(self.client), self.cmd_data[1:]
        raise CommandNotExist()
