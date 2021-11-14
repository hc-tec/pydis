

class NoImplError(Exception):
    pass


class BaseCommand:

    help = ''

    def __init__(self, client):
        self.client = client

    def execute(self, *args, **kwargs):
        raise NoImplError()

    def get_help(self):
        return self.help


class CommandHandler:

    def __init__(self, client):
        self.client = client
        self.raw_command_data = client.query_buffer.pop()

    def parse_command(self) -> BaseCommand:
        pass



