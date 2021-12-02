
from typing import Optional, List, Dict

from Client.interfaces import IClient
from Generic.utils import generate_uuid
from Generic.socket import socket_connect
from Sentinel.base import SRI_TYPE
from Sentinel.interfaces import ISentinelManager, ISentinelRedisInstance
from Sentinel.instance import SentinelRedisInstance


class SentinelManager(ISentinelManager):

    def __init__(self):

        self._id = generate_uuid()
        self._current_epoch = 0
        self._masters: Dict[str, ISentinelRedisInstance] = {}
        self._announce_ip = None
        self._announce_port = 0

        self.message_connection: Optional[IClient] = None
        self.command_connection: Optional[IClient] = None
        self.message_conn_list: List[IClient] = []
        self.command_conn_list: List[IClient] = []

    def get_command_connection(self) -> List[IClient]:
        return self.command_conn_list

    def get_message_connection(self) -> List[IClient]:
        return self.message_conn_list

    def get_master_message_connection(self) -> IClient:
        return self.message_connection

    def set_message_connection(self, message_connection: IClient):
        self.message_connection = message_connection
        self.message_conn_list.append(message_connection)

    def get_master_command_connection(self) -> IClient:
        return self.command_connection

    def set_command_connection(self, command_connection: IClient):
        self.command_connection = command_connection
        self.command_conn_list.append(command_connection)

    def append_message_connection(self, message_connection: IClient):
        self.message_conn_list.append(message_connection)

    def append_command_connection(self, command_connection: IClient):
        self.command_conn_list.append(command_connection)

    @staticmethod
    def sentinel_message_conn(master_addr: tuple, server, sentinel_manager: ISentinelManager):
        # 消息连接
        conn = socket_connect(*master_addr)
        message_conn = server.connect_from_self(conn)
        sentinel_manager.set_message_connection(message_conn)
        message_conn.append_reply_enable_write('subscribe __sentinel__:hello\n')

    @staticmethod
    def sentinel_command_conn(master_addr: tuple, server, sentinel_manager: ISentinelManager):
        # 命令连接
        conn = socket_connect(*master_addr)
        command_conn = server.connect_from_self(conn)
        sentinel_manager.set_command_connection(command_conn)

    def build_redis_instance(self, server, info: dict):
        instance = self._masters.get(info['run_id'])
        if not instance:
            build_func = getattr(self, f'_build_{info["role"]}_redis_instance')
            build_func(server, info)
            return
        modify_func = getattr(self, f'_modify_{info["role"]}_redis_instance')
        modify_func(server, instance, info)
        print(instance)

    def _build_master_redis_instance(self, server, info: dict):
        instance = SentinelRedisInstance(info=info, **info)
        self._masters[info['run_id']] = instance
        if int(info['connected_slaves']):
            self.connect_slaves(server, info['slaves_host'])

    def _build_slave_redis_instance(self, server, info: dict):
        instance = SentinelRedisInstance(info=info, **info)
        self._masters[info['run_id']] = instance

    def _modify_master_redis_instance(self, server, instance: ISentinelRedisInstance, info: dict):
        instance.modify(info=info, **info)
        origin_info = instance.get_info()
        if int(info['connected_slaves']):
            origin_slaves: set = origin_info['slaves_host']
            current_slaves: set = info['slaves_host']
            diff = current_slaves.difference(origin_slaves)
            self.connect_slaves(server, diff)

    def _modify_slave_redis_instance(self, server, instance: ISentinelRedisInstance, info: dict):
        instance.modify(info=info, **info)

    def connect_slaves(self, server, slave_host_set: set):
        sentinel_manager = server.get_sentinel_manager()
        for host in slave_host_set:
            self.sentinel_command_conn(host, server, sentinel_manager)
            self.sentinel_message_conn(host, server, sentinel_manager)
