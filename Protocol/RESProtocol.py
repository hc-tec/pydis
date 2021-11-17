

class RESProtocol:

    def __init__(self, raw_data):
        self.__raw_data: str = raw_data.strip()

    def parse(self):
        return self.__raw_data.lower()
