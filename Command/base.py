

from typing import Dict, Any, List

from Conf.command import CMD_RES
from Command.exception import CommandArgsNumInvalid, NoImplError
from Command.interfaces import ICommand

COMMAND_MIN_ARGS_NUM = 0
COMMAND_MAX_ARGS_NUM = 9999


class CommandType:
    CMD_READ = 1
    CMD_WRITE = 1 << 2
    CMD_COMMON = 1 << 3
    CMD_NONE = 1 << 4


class BaseCommand(ICommand):

    help = ''
    cmd_type = CommandType.CMD_COMMON
    min_args = COMMAND_MIN_ARGS_NUM
    max_args = COMMAND_MAX_ARGS_NUM
    args_order = []
    need_kwargs = True

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
        if self.need_kwargs:
            kwargs = self.parse_args(*args)
        result = self.handle(*args, kwargs)
        if not isinstance(result, CMD_RES):
            return result or '(nil)'
        elif result == CMD_RES.OK:
            return '(ok)'

    def handle(self, args, kwargs):
        raise NoImplError()

    def get_help(self):
        return self.help
