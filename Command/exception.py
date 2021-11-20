
from Exception.base import BaseError


class NoImplError(BaseError):
    msg = 'Command is not implement\n'


class CommandNotExist(BaseError):
    msg = 'Command is not exist\n'


class CommandArgsNumInvalid(BaseError):
    msg = 'Command args num is invalid\n'


class DiscardWithoutMultiError(BaseError):

    msg = 'DISCARD without MULTI\n'


class ExecWithoutMultiError(BaseError):

    msg = 'EXEC without MULTI\n'

