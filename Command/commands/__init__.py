
from .get import Get
from .set import Set
from .ping import Ping
from .slaveof import SlaveOf
from .sync import Sync
from .bgsave import BgSave

from .replconf import ReplConf

COMMAND_DICT = {
    'get': Get,
    'set': Set,
    'ping': Ping,
    'slaveof': SlaveOf,
    'sync': Sync,
    'bgsave': BgSave,

    'replconf': ReplConf,
}

