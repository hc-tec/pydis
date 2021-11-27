

from typing import Optional
from socket import socket

from Client.base import CLIENT_FLAG
from Client.interfaces import IClientHandler, IClient
from Client.handler import BaseHandler
from Connection import Connection
from Connection.interfaces import IConnection
from Command.handler import CommandHandler
from Command.interfaces import ICommand
from Database.interfaces import IDatabase
from Generic.time import get_cur_time
from Generic.patterns.observer import Observer
from Generic.decoration import alias
from IOLoop.reader import Reader
from IOLoop.writer import Writer
from IOLoop.interfaces import IReader, IWriter
from Protocol import RESProtocol
from Pubsub.channel import Channel
from Pubsub.manager import PubsubClientManager
from Pubsub.interfaces import IPubsubClientManager
from Replication.manager import ReplClientManager
from Replication.interfaces import IReplClientManager
from Server.interfaces import IServer
from Transaction.manager import TransactionManager
from Transaction.interfaces import ITransactionManager


class Client(IClient):

    def __init__(self, server: IServer, client_id: int, db: IDatabase, sock: socket):
        self._server = server
        self._id = client_id
        self._db = db
        self._conn = Connection(sock, server.get_loop())
        self._reader = Reader()
        self._writer = Writer()
        self._handler: IClientHandler = BaseHandler()
        self._repl_manager = ReplClientManager()

        self.flag = CLIENT_FLAG.MASTER


        self.current_command: Optional[ICommand] = None
        self.create_time = get_cur_time()
        self.last_interaction = None
        self.authenticated = True

        self._transaction_manager = TransactionManager()
        self._pubsub_manager = PubsubClientManager()


    def get_database(self) -> IDatabase:
        return self._db

    def get_connection(self) -> IConnection:
        return self._conn

    def get_reader(self) -> IReader:
        return self._reader

    def get_writer(self) -> IWriter:
        return self._writer

    def get_handler(self) -> IClientHandler:
        return self._handler

    def get_repl_manager(self) -> IReplClientManager:
        return self._repl_manager

    def get_transaction_manager(self) -> ITransactionManager:
        return self._transaction_manager

    def get_pubsub_manager(self) -> IPubsubClientManager:
        return self._pubsub_manager

    def transform_handler(self, handler: IClientHandler):
        self._handler = handler

    def read_from_client(self):
        read_data = self._reader.read_from_conn(self._conn)
        if not read_data or CommandHandler.is_valid_command(read_data): return

        self._handler.data_received(read_data, client=self)

    def write_to_client(self) -> int:
        res = self._writer.write_to_client(self._conn)
        if res == 0:
            self.flag = CLIENT_FLAG.CLOSE_ASAP
            self.close()
        return res

    def append_reply(self, reply):
        self._writer.append_reply(reply)

    def append_reply_enable_write(self, reply):
        self._writer.append_reply(reply)
        self._conn.enable_write()

    def handle_command_after_resp(self, cmd_data):
        cmd_data = RESProtocol(cmd_data).parse()
        self.handle_command(cmd_data)

    def handle_command(self, cmd_data):
        handler = CommandHandler(self, cmd_data)
        handler.handle()
        if not self._writer.is_reply_empty():
            self._conn.enable_write()
    # def switch_IDatabase(self, db_index):
    #     self.db = server.get_IDatabase(db_index)
    #
    def get_server(self) -> IServer:
        return self._server

    def set_current_command(self, command: Optional[ICommand]) -> bool:
        self.current_command = command
        return self._handler.command_executed_before(command, self)

    def touch_watched_key(self, command: ICommand):
        key = command.raw_cmd.split()[1]
        # if key is watched, changes watching client flag
        clients = self._db.withdraw_watch_keys(key)
        if clients:
            for client in clients:
                if client.flag & CLIENT_FLAG.CLOSE_ASAP:
                    clients.remove(client)
                    continue
                client.flag |= CLIENT_FLAG.DIRTY_CAS

    @alias(Observer, 'update')
    def receive_notice_from_subscribe_channel(self, channel: Channel):
        if self.flag & CLIENT_FLAG.CLOSE_ASAP:
            channel.detach(self)
            self.close()
            return
        self.append_reply_enable_write(f'{channel.message}\n')

    def close(self):
        self._conn.connect_close()

    def __str__(self):
        return '<{} id={} flag={} repl_state={} repl_ack_time={}>'.format(
            self.__class__.__name__,
            self._id,
            self.flag,
            self.get_repl_manager().get_repl_state(),
            self.get_repl_manager().get_repl_ack_time(),
        )

    __repr__ = __str__

