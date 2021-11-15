
from typing import Dict, Any, List

from Exception.base import BaseError

COMMAND_MIN_ARGS_NUM = 0
COMMAND_MAX_ARGS_NUM = 9999


class BaseCommandError(BaseError):
    msg = 'Command Error'


class NoImplError(BaseCommandError):
    msg = 'Command is not implement\n'


class CommandNotExist(BaseCommandError):
    msg = 'Command is not exist\n'


class CommandArgsNumInvalid(BaseCommandError):
    msg = 'Command args num is invalid\n'


class BaseCommand:

    help = ''

    min_args = COMMAND_MIN_ARGS_NUM
    max_args = COMMAND_MAX_ARGS_NUM
    args_order = []

    def __init__(self, client):
        self.client = client

    def check_arg_num(self, arg_len: int) -> bool:
        return self.min_args <= arg_len <= self.max_args

    def parse_args(self, args: List[Any]) -> Dict[str, Any]:
        if not self.check_arg_num(len(args)):
            raise CommandArgsNumInvalid()
        kwargs = {}
        for index, value in enumerate(args):
            arg = self.args_order[index]
            kwargs[arg] = value
        return kwargs

    def execute(self, *args, **kwargs):
        args = self.parse_args(*args)
        return self.handle(args)

    def handle(self, args):
        raise NoImplError()

    def get_help(self):
        return self.help


