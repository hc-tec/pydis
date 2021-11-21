
from .get import Get
from .set import Set
from .ping import Ping
from .slaveof import SlaveOf
from .sync import Sync
from .bgsave import BgSave

from .multi import Multi
from .exec import Exec
from .discard import Discard
from .watch import Watch
from .unwatch import UnWatch

from .publish import Publish
from .subscribe import Subscribe
from .unsubscribe import Unsubscribe

from .replconf import ReplConf

COMMAND_DICT = {
    'get': Get,
    'set': Set,
    'ping': Ping,
    'slaveof': SlaveOf,
    'sync': Sync,
    'bgsave': BgSave,

    'multi': Multi,
    'exec': Exec,
    'discard': Discard,
    'watch': Watch,
    'unwatch': UnWatch,

    'publish': Publish,
    'subscribe': Subscribe,
    'unsubscribe': Unsubscribe,

    'replconf': ReplConf,
}

