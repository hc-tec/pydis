

from socket import socket
from typing import List, Optional


from Client.manager import ClientManager
from Client.interfaces import IClient
from Client.handler import SlaveHandler
from Cluster.interfaces import IClusterManager
from Cluster.manager import ClusterManager
from Conf import app, sentinel
from IOLoop.Reactor.interfaces import IReactor
from IOLoop.Reactor.event import ReEvent
from Database.interfaces import IDatabaseManager
from Database.persistence.manager import PersistenceManager
from Database.persistence.base import PERS_STATUS
from Database.persistence.interfaces import IRDBManager, IAOFManager, IPersistenceManager
from Database.manager import DatabaseManager
from Generic.time import get_cur_time
from Generic.file import read_file
from Generic.socket import socket_connect
from Generic.utils import generate_uuid
from Replication.slave import REPL_SLAVE_STATE
from Replication.manager import ReplServerMasterManager, ReplServerSlaveManager
from Replication.interfaces import IReplServerMasterManager, IReplServerSlaveManager
from Pubsub.manager import PubsubServerManager
from Pubsub.interfaces import IPubsubServerManager
from Server.base import SERVER_FLAG
from Server.interfaces import IServer
from Sentinel.manager import SentinelManager
from Sentinel.interfaces import ISentinelManager
from Timer.timestamp import Timestamp
from Timer.event import TimeoutEvent


SETTINGS = app.get_settings()


class Server(IServer):

    def __init__(self):

        self._id = generate_uuid()
        self._create_time = get_cur_time()

        self.flag = SERVER_FLAG.COMMON

        self.__loop: Optional[IReactor] = None

        self._database_manager = DatabaseManager()
        self._persistence_manager = PersistenceManager()
        self._client_manager = ClientManager()

        self._repl_master_manager = ReplServerMasterManager()
        self._repl_slave_manager = ReplServerSlaveManager()

        self._pubsub_manager = PubsubServerManager()

        self._sentinel_manager: Optional[ISentinelManager] = None

        self._cluster_manager: IClusterManager = ClusterManager()

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

    def is_sentinel_mode(self) -> bool:
        return self.flag & SERVER_FLAG.SENTINEL

    def on_sentinel_mode(self):
        self.flag |= SERVER_FLAG.SENTINEL
        self._sentinel_manager = SentinelManager()

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

    def get_sentinel_manager(self) -> ISentinelManager:
        return self._sentinel_manager

    def load_persistence_file(self):
        self.get_rdb_manager().load_file(self._database_manager)

    def write_cmd_increment(self):
        self.get_rdb_manager().incr_dirty()

    def incr_watchdog_run_num(self):
        self.watchdog_run_num += 1

    def start_watchdog(self):
        # execute per WATCH_DOG_CYCLE(ms)
        timestamp = Timestamp(SETTINGS.WATCH_DOG_CYCLE)
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

        client = self.connect_from_self(conn)
        slave_handler = SlaveHandler()
        slave_handler.set_slaveof_cmd_sender(slaveof_cmd_sender)
        client.transform_handler(slave_handler)
        slave_handler.replicate(client)
        self._repl_slave_manager.set_master(client)

    def connect_from_self(self, conn: socket) -> IClient:
        self.get_loop().get_poller().register(conn.fileno(), ReEvent.RE_WRITABLE)
        return self.connect_from_client(conn)

    def read_from_client(self, fd):
        return self._client_manager.read_from_client(fd)

    def write_to_client(self, fd):
        return self._client_manager.write_to_client(fd)

    def upgrade_client_to_master(self, client: IClient):
        self._repl_master_manager.append_slaves(client)

    def EVERY_SECOND(self, second=1):
        # return True when {second}s pass, default 1s
        return self.watchdog_run_num % (1000 * second // SETTINGS.WATCH_DOG_CYCLE) == 0

    def info(self, section=None):
        server = f'''redis_version: {SETTINGS.__version__}
run_id: {self._id}
tcp_ip: {self.host}
tcp_port: {self.port}
uptime_in_seconds: {(get_cur_time() - self._create_time) // 1000}
'''
        slaves_num = self._repl_master_manager.get_slaves_num()
        clients = f'''
connected_clients: {self._client_manager.get_client_num() - slaves_num}
client_longest_output_list: 1
client_longest_input_buf: 1
blocked_clients: 1
'''
        role = 'master' if self._repl_slave_manager.get_master() is None else 'slave'

        replication = f'''
role: {role}
connected_slaves: {slaves_num}
{self._repl_master_manager.get_slaves_host()}
'''
        return server + clients + replication



class ServerWatchDog(TimeoutEvent):

    def handle_event(self, reactor):
        server: IServer = self.extra_data
        # print('watch dog')
        if server.is_sentinel_mode():
            self.sentinel_timer(server)
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
            if repl_master_manager.need_sync():
                self.sync_with_slaves(server)
                repl_master_manager.sync_disable()

    def sync_with_slaves(self, server: IServer):
        rdb_manager = server.get_rdb_manager()
        repl_master_manager = server.get_repl_master_manager()
        rdb_file_data = read_file(rdb_manager.get_file_path())
        for slave in repl_master_manager.get_slaves():
            slave: IClient = slave
            if slave.get_repl_manager().get_repl_state() == REPL_SLAVE_STATE.TRANSFER:
                slave.append_reply_enable_write(rdb_file_data + '\n')

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
        if not server.EVERY_SECOND(): return

        if aof_manager.get_buffer():
            server.start_aof()

    def keep_alive_with_slaves(self, server: IServer):
        repl_master_manager = server.get_repl_master_manager()

        slaves: List[IClient] = repl_master_manager.get_connected_slaves()
        if not slaves: return

        period = repl_master_manager.get_repl_ping_slave_period()
        if not server.EVERY_SECOND(period): return
        for slave in slaves:
            slave.append_reply_enable_write('PING\n')

    def sentinel_timer(self, server: IServer):
        if not (server.flag & SERVER_FLAG.SENTINEL_CONNECT_MASTER):
            self.connect_with_master(server)
        self.message_conn_timer(server)
        self.command_conn_timer(server)

    def connect_with_master(self, server: IServer):
        master_addr = SETTINGS.SENTINEL_MASTER_ADDR
        sentinel_manager = server.get_sentinel_manager()
        SentinelManager.sentinel_message_conn(master_addr, server, sentinel_manager)
        SentinelManager.sentinel_command_conn(master_addr, server, sentinel_manager)
        server.flag |= SERVER_FLAG.SENTINEL_CONNECT_MASTER

    def command_conn_timer(self, server: IServer):
        sentinel_manager = server.get_sentinel_manager()
        # info command
        self.sentinel_command_task(sentinel.COMMAND_CONN_INFO_CYCLE, 'info', sentinel_manager)
        # ping command
        self.sentinel_command_task(sentinel.COMMAND_CONN_PING_CYCLE, 'ping', sentinel_manager)
        # self-info
        # self.sentinel_command_task(sentinel.COMMAND_CONN_SELF_CYCLE, '', sentinel_manager)

    def message_conn_timer(self, server: IServer):
        ...

    def sentinel_command_task(self, cycle: int, message: str, sentinel_manager: ISentinelManager):
        if server.EVERY_SECOND(cycle):
            connections = sentinel_manager.get_command_connection()
            for conn in connections:
                conn.append_reply_enable_write(f'{message}\n')


server = Server()

