

class ReServer:

    def __init__(self):
        self.__next_client_id = 1
        self.__loop = None
        self.__clients = {}
        self.__slaves = []
        self.__monitors = []
        self.__current_client = None

        # RDB / AOF
        self.loading = False

        # Configuration
        self.db_num = 16

        # Limits
        self.max_clients = 1000

    @property
    def next_client_id(self):
        self.__next_client_id += 1
        return self.__next_client_id

    def set_loop(self, loop):
        self.__loop = loop


