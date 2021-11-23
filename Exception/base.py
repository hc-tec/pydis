

class BaseError(Exception):
    msg = 'Server Error'

    def get_msg(self):
        return f'{self.msg}\n'

