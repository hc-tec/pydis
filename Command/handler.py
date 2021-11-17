
from typing import List, Tuple

from .commands import COMMAND_DICT
from .base import BaseCommand, CommandNotExist
from Exception.base import BaseError
from Conf.command import CMD_RES


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
            self.client.set_current_command(command)
            result = command.execute(args)
            if not isinstance(result, CMD_RES):
                self.client.append_reply(result+'\n')
            elif result == CMD_RES.OK:
                self.client.append_reply('(ok) \n')
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
