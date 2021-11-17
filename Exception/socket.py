
from Exception.base import BaseError


class ConnectionRefuseError(BaseError):

    def __init__(self, host, port):
        self.msg = f'Could not connect to Redis at {host}:{port}: Connection refused'
