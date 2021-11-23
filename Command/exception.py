
from Exception.base import BaseError


class NoImplError(BaseError):
    msg = 'Command is not implement'


class CommandNotExist(BaseError):
    msg = 'Command is not exist'


class CommandArgsNumInvalid(BaseError):
    msg = 'Command args num is invalid'


class DiscardWithoutMultiError(BaseError):

    msg = 'DISCARD without MULTI'


class ExecWithoutMultiError(BaseError):

    msg = 'EXEC without MULTI'

