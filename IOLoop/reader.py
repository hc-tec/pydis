
from Connection.interfaces import IConnection
from Protocol import RESProtocol
from IOLoop.interfaces import IReader


class Reader(IReader):

    def __init__(self):
        self._query_buffer = ''
        # self._query_cursor = 0
        self._read_data = ''

    def is_command_input_end(self) -> bool:
        print(self._query_buffer)
        return self._query_buffer.endswith('\n')

    def clear_read_data(self):
        self._read_data = ''

    def read_from_conn(self, conn: IConnection) -> str:
        raw_read_data = conn.data_received()
        self._query_buffer += raw_read_data
        if self.is_command_input_end():
            # self.query_cursor += len(self.query_buffer)
            self._read_data = RESProtocol(self._query_buffer).parse()
            self._query_buffer = ''
            # self.query_cursor = 0
        return self._read_data






