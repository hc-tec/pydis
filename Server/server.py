
from socket import socket
from typing import Dict, List

from Client import Client
from Connection import Connection
from Database import Database
from Database.persistence.base import PERS_STATUS
from Database.persistence.RDB import RDB
from Database.persistence.AOF import AOF, AOF_FSYNC_TYPE
from Server.exception import DatabaseNotExistError
from Timer.timer import SaveParam
from Timer.timestamp import Timestamp
from Timer.event import TimeoutEvent
from Generic.time import get_cur_time
from Generic.server import generate_uuid
from Generic.file import read_file
from Conf import app
from Replication.slave import SlaveClient, REPL_SLAVE_STATE


SETTINGS = app.get_settings()


class Server:

    def __init__(self):
        self.__next_client_id = 1
        self.__loop = None
        self.__clients: Dict[int, Client] = {}
        self.__slaves = []
        self.__monitors = []
        self.__current_client = None
        self.__databases: List[Database] = []

        self.watchdog_run_num = 0

        self.host = None
        self.port = None

        # persistence status
        self.pers_status = PERS_STATUS.NO_WRITE

        # RDB persistence
        self.rdb_enable = True
        self.save_params: List[SaveParam] = [
            SaveParam(900, 1),
            SaveParam(300, 10),
            SaveParam(3, 1)
        ]
        self.dirty = 0
        self.dirty_before_bgsave = get_cur_time()
        self.rdb_filename = SETTINGS.RDB_FILE
        self.rdb_compression = False
        self.rdb_checksum = 0

        self.last_save = None
        self.rdb_save_time_start = 0


        # AOF Persistence
        self.aof_enable = True
        self.aof_fsync = AOF_FSYNC_TYPE.EVERY_SECOND
        self.aof_filename = SETTINGS.AOF_FILE
        self.aof_buf = []
        self.aof_rewrite_last_time = get_cur_time()

        # Replication (master)
        self.repl_id = generate_uuid()
        self.repl_ping_slave_period = 10 # Master pings the slave every N seconds
        self.repl_good_slaves_count = 0
        self.repl_min_slaves_to_write = 0
        self.repl_min_slaves_max_lag = 10
        self.repl_slaves: List[Client] = []
        self.need_sync = False

        # Replication (slave)
        self.master_host = None
        self.master_port = None
        self.master = None
        self.repl_state = REPL_SLAVE_STATE.NONE
        self.repl_slave_ro = True

        # Configuration
        self.db_num = 16

        # Limits
        self.max_clients = 1000

        self.create_databases()
        self.load_persistent_file()

    def set_host(self, host, port):
        self.host = host
        self.port = port

    def write_cmd_increment(self):
        self.dirty +=  1

    def start_watchdog(self):
        # execute per 100ms
        timestamp = Timestamp(100)
        watchdog_event = ServerWatchDog(timestamp)
        watchdog_event.set_extra_data(self)
        self.get_loop().create_timeout_event(watchdog_event)

    def create_databases(self):
        for i in range(self.db_num):
            self.__databases.append(Database(i))

    def get_database(self, index=0) -> Database:
        # default database: db[0]
        if 0 <= index < self.db_num:
            return self.__databases[index]
        raise DatabaseNotExistError(index)

    def get_databases(self):
        return self.__databases

    @property
    def next_client_id(self):
        self.__next_client_id += 1
        return self.__next_client_id

    def set_loop(self, loop):
        self.__loop = loop

    def get_loop(self):
        return self.__loop

    def connect_from_client(self, conn: socket):
        connection = Connection(conn, self.__loop)
        client = Client(self, self.next_client_id, self.get_database(), connection)
        self.__clients[conn.fileno()] = client

    def connect_to_master(self, conn: socket, addr, origin_client: Client):
        self.get_loop().get_acceptor()._handle_accept(
            conn,
            addr,
            self.get_loop().events,
            self.get_loop().get_poller()
        )
        connection = Connection(conn, self.__loop)
        slave = SlaveClient(self, self.next_client_id, self.get_database(), connection, origin_client=origin_client)
        self.master = slave
        self.__clients[conn.fileno()] = slave

    def read_from_client(self, fd):
        client = self.__clients[fd]
        client.read_from_client()

    def write_to_client(self, fd):
        client = self.__clients[fd]
        client.write_to_client()

    def rdb_reset(self):
        self.dirty = 0
        self.dirty_before_bgsave = get_cur_time()

    def rdb_start(self):
        rdb = RDB(self.rdb_filename)
        rdb.save(self)
        self.rdb_reset()

    def aof_start(self):
        aof = AOF(self.aof_filename)
        aof.save(self)

    def load_persistent_file(self):
        rdb = RDB(SETTINGS.RDB_FILE)
        rdb.load(self)

    def load_from_master(self, data):
        rdb = RDB(None)
        rdb.load_from_data(self, data)


class ServerWatchDog(TimeoutEvent):

    def handle_event(self, reactor):
        server: Server = self.extra_data
        # print('watch dog')

        self.process_persistence(server)
        self.check_persistence_status(server)

        # restart watchdog when finish execution
        server.start_watchdog()
        server.watchdog_run_num += 1

    def check_persistence_status(self, server):
        if server.pers_status & PERS_STATUS.WRITED:
            print('persistence finish')
            server.pers_status = PERS_STATUS.NO_WRITE
            server.last_save = get_cur_time()
            # TODO: notify client persistence finished
            if server.need_sync:
                rdb_file_data = read_file(server.rdb_filename)
                for slave in server.repl_slaves:
                    if slave.repl_state == REPL_SLAVE_STATE.TRANSFER:
                        slave.append_reply(rdb_file_data+'\n')
                        slave.conn.enable_write()
                server.need_sync = False

    def process_persistence(self, server: Server):

        self.process_rdb(server)
        self.process_aof(server)


    def process_rdb(self, server):
        if not server.rdb_enable: return

        for save_param in server.save_params:
            if server.dirty >= save_param.changes and \
                    get_cur_time() - server.dirty_before_bgsave >= save_param.seconds:
                server.rdb_start()
                break

    def process_aof(self, server):
        if not server.aof_enable: return

        if server.watchdog_run_num % 10 != 0: return
        if server.aof_buf:
            server.aof_start()


server = Server()

