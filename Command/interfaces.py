
from abc import ABCMeta, abstractmethod
from typing import Tuple, List, Dict, Any


class ICommand(metaclass=ABCMeta):

    raw_cmd = ''
    cmd_type = ''

    @abstractmethod
    def check_arg_num(self, arg_len: int) -> bool:
        ...

    @abstractmethod
    def execute(self, *args, **kwargs):
        ...

    @abstractmethod
    def handle(self, args, kwargs):
        ...

    @abstractmethod
    def get_help(self):
        ...

    @abstractmethod
    def parse_args(self, args: List[Any]) -> Dict[str, Any]:
        ...


class ICommandHandler(metaclass=ABCMeta):

    @abstractmethod
    def handle(self):
        ...

    @abstractmethod
    def parse_command(self) -> Tuple[ICommand, List]:
        ...


class ICommandCaller(metaclass=ABCMeta):

    @abstractmethod
    def handle_command(self, cmd_data):
        ...


class ICommandManager(metaclass=ABCMeta):

    @abstractmethod
    def set_current_command(self, command: ICommand) -> bool:
        ...
