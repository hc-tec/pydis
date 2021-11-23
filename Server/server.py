

from socket import socket
from typing import Dict, List, Optional, Union

from interfaces import ISyncAble
from Client import Client
from Client.manager import ClientManager
from Client.interfaces import IClient, IClientHandler
from Client.handler import SlaveHandler
from IOLoop.Reactor.interfaces import IReactor
from Database.interfaces import IDatabaseManager
from Database.persistence.manager import PersistenceManager
from Database.persistence.base import PERS_STATUS
from Database.persistence.interfaces import IRDBManager, IAOFManager, IPersistenceManager
from Database.manager import DatabaseManager

from Timer.timestamp import Timestamp
from Timer.event import TimeoutEvent
from Generic.time import get_cur_time

from Generic.file import read_file
from Conf import app
from Replication.slave import REPL_SLAVE_STATE
from Replication.manager import ReplServerMasterManager, ReplServerSlaveManager
from Replication.interfaces import IReplServerMasterManager, IReplServerSlaveManager
from Pubsub.manager import PubsubServerManager
from Pubsub.interfaces import IPubsubServerManager
from Server.interfaces import IServer


SETTINGS = app.get_settings()


class Server(IServer):

    def __init__(self):

        self.__loop: Optional[IReactor] = None

        # self.__slaves = []
        # self.__monitors = []

        self._database_manager = DatabaseManager()
        self._persistence_manager = PersistenceManager()
        self._client_manager = ClientManager()

        self._repl_master_manager = ReplServerMasterManager()
        self._repl_slave_manager = ReplServerSlaveManager()

        self._pubsub_manager = PubsubServerManager()

        self.watchdog_run_num = 0

        self.host = None
        self.port = None



        self.load_persistence_file()

    def set_addr(self, host, port):
        self.host = host
        self.port = port

    def get_addr(self) -> dict:
        return {
            'host': self.host,
            'port': self.port
        }

    def get_database_manager(self) -> IDatabaseManager:
        return self._database_manager

    def get_persistence_manager(self) -> IPersistenceManager:
        return self._persistence_manager

    def get_rdb_manager(self) -> IRDBManager:
        return self._persistence_manager.get_rdb_manager()

    def get_aof_manager(self) -> IAOFManager:
        return self._persistence_manager.get_aof_manager()

    def get_repl_master_manager(self) -> IReplServerMasterManager:
        return self._repl_master_manager

    def get_repl_slave_manager(self) -> IReplServerSlaveManager:
        return self._repl_slave_manager

    def get_pubsub_manager(self) -> IPubsubServerManager:
        return self._pubsub_manager

    def load_persistence_file(self):
        self.get_rdb_manager().load_file(self._database_manager)

    def write_cmd_increment(self):
        self.get_rdb_manager().incr_dirty()

    def incr_watchdog_run_num(self):
        self.watchdog_run_num += 1

    def start_watchdog(self):
        # execute per WATCH_DOG_INTERVAL(ms)
        timestamp = Timestamp(SETTINGS.WATCH_DOG_INTERVAL)
        watchdog_event = ServerWatchDog(timestamp)
        watchdog_event.set_extra_data(self)
        self.get_loop().create_timeout_event(watchdog_event)

    def start_aof(self):
        self.get_aof_manager().start(self._database_manager, self._persistence_manager)

    def start_rdb(self):
        self.get_rdb_manager().start(self._database_manager, self._persistence_manager)

    def set_loop(self, loop: IReactor):
        self.__loop = loop

    def get_loop(self) -> IReactor:
        return self.__loop

    def connect_from_client(self, conn: socket) -> IClient:
        return self._client_manager.connect_from_client(self, self._database_manager.get_database(), conn)

    def connect_to_master(self, conn: socket, slaveof_cmd_sender: IClient):

        self.get_loop().get_acceptor().connected(
            conn.fileno(),
        )
        client = self.connect_from_client(conn)
        slave_handler = SlaveHandler()
        slave_handler.set_slaveof_cmd_sender(slaveof_cmd_sender)
        client.transform_handler(slave_handler)
        slave_handler.replicate(client)

    def read_from_client(self, fd):
        return self._client_manager.read_from_client(fd)

    def write_to_client(self, fd):
        return self._client_manager.write_to_client(fd)

    def upgrade_client_to_master(self, client: IClient):
        print('upgrade')
        # master = MasterClient()
        # # copy from client
        # master.upgrade_from_client(client)
        self._repl_master_manager.append_slaves(client)
        # replace common client with master client
        # self.__clients[client.conn.get_sock_fd()] = master

    def EVETY_SECOND(self, second=1):
        # return True when {second}s pass, default 1s
        return self.watchdog_run_num % (1000 * second // SETTINGS.WATCH_DOG_INTERVAL) == 0


class ServerWatchDog(TimeoutEvent):

    def handle_event(self, reactor):
        server: IServer = self.extra_data
        # print('watch dog')

        self.process_persistence(server)
        self.check_persistence_status(server)
        self.keep_alive_with_slaves(server)
        # restart watchdog when finish execution
        server.start_watchdog()
        server.incr_watchdog_run_num()

    def check_persistence_status(self, server: IServer):
        persist_manager = server.get_persistence_manager()
        repl_master_manager = server.get_repl_master_manager()
        if persist_manager.get_pers_status() & PERS_STATUS.WRITED:
            print('persistence finish')
            persist_manager.set_pers_status(PERS_STATUS.NO_WRITE)
            # notify client persistence finished
            if repl_master_manager.get_sync():
                self.sync_with_slaves(server)

    def sync_with_slaves(self, server: IServer):
        rdb_manager = server.get_rdb_manager()
        repl_master_manager = server.get_repl_master_manager()
        rdb_file_data = read_file(rdb_manager.get_file_path())
        for slave in repl_master_manager.get_slaves():
            if slave.get_repl_manager().get_repl_state() == REPL_SLAVE_STATE.TRANSFER:
                slave.append_reply_enable_write(rdb_file_data + '\n')
        repl_master_manager.sync_disable()

    def process_persistence(self, server: IServer):

        self.process_rdb(server)
        self.process_aof(server)

    def process_rdb(self, server: IServer):

        rdb_manager = server.get_rdb_manager()

        if not rdb_manager.is_enable(): return

        for save_param in rdb_manager.get_save_params():
            if rdb_manager.get_dirty() >= save_param.changes and \
                    get_cur_time() - rdb_manager.get_dirty_before_bgsave() >= save_param.seconds:
                server.start_rdb()
                break

    def process_aof(self, server: IServer):

        aof_manager = server.get_aof_manager()

        if not aof_manager.is_enable(): return
        if not server.EVETY_SECOND(): return

        if aof_manager.get_buffer():
            server.start_aof()

    def keep_alive_with_slaves(self, server: IServer):
        repl_master_manager = server.get_repl_master_manager()

        slaves: List[IClient] = repl_master_manager.get_connected_slaves()
        if not slaves: return

        period = repl_master_manager.get_repl_ping_slave_period()
        if not server.EVETY_SECOND(period): return
        for slave in slaves:
            print(slave)
            slave.append_reply_enable_write('PING\n')

server = Server()

