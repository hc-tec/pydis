

from typing import Dict, Any, List

from Exception.base import BaseError

COMMAND_MIN_ARGS_NUM = 0
COMMAND_MAX_ARGS_NUM = 9999


class CommandType:
    CMD_READ = 0
    CMD_WRITE = 1
    CMD_COMMON = 2
    CMD_NONE = 4


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
    cmd_type = CommandType.CMD_COMMON
    min_args = COMMAND_MIN_ARGS_NUM
    max_args = COMMAND_MAX_ARGS_NUM
    args_order = []

    def __init__(self, client, raw_cmd):
        self.client = client
        self.raw_cmd = raw_cmd

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


