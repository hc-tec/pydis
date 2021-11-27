

from Client.handler import BaseHandler
from Client.interfaces import IClient


class SentinelHandler(BaseHandler):

    def data_received(self, data, client: IClient):
        self.handle_command(data, client)














