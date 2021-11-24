
from typing import List, Tuple

from Client.interfaces import IClient
from Command.commands import COMMAND_DICT
from Command.base import BaseCommand
from Command.exception import CommandNotExist
from Command.interfaces import ICommandHandler, ICommand
from Exception.base import BaseError
from Client.base import CLIENT_FLAG


class CommandHandler(ICommandHandler):

    def __init__(self, client: IClient, cmd_data):
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
                if self.is_multi_on(command):
                    transaction_manager = self.client.get_transaction_manager()
                    transaction_manager.append_to_buffer((command, args))
                    self.client.append_reply('QUEUED\n')
                elif self.is_pubsub_on(command):
                    self.client.append_reply('only (P)SUBSCRIBE / (P)UNSUBSCRIBE / PING / QUIT allowed in this context\n')
                else:
                    result = command.execute(args)
                    if result is not None:
                        self.client.append_reply(f'{result}\n')

        except BaseError as e:
            self.client.append_reply(e.get_msg())
        finally:
            self.client.set_current_command(None)

    def is_multi_on(self, command: ICommand):
        multi_flag_on = self.client.flag & CLIENT_FLAG.MULTI
        multi_allowed_commands = ['multi', 'exec', 'discard', 'watch']
        return multi_flag_on and \
               not multi_allowed_commands.__contains__(command.__class__.__name__.lower())

    def is_pubsub_on(self, command: ICommand):
        pubsub_flag_on = self.client.flag & CLIENT_FLAG.PUBSUB
        pubsub_allowed_commands = ['ping', 'subscribe', 'unsubscribe',
                                   'psubscribe', 'punsubscribe']
        return pubsub_flag_on and \
                not pubsub_allowed_commands.__contains__(command.__class__.__name__.lower())

    def parse_command(self) -> Tuple[ICommand, List]:
        try:
            self.cmd_name = self.cmd_data[0]
        except IndexError:
            pass
        command = self.is_cmd_exist()
        if command:
            return command(self.client, self.raw_cmd), self.cmd_data[1:]
        raise CommandNotExist()
