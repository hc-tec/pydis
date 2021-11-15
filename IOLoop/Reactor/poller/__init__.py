

from .base import Poller
from .Epoll import Epoll
from .Select import Select

from Generic.runtime import platform

SYS_POLLER_DICT = {
    'win': Select,
    'linux': Epoll,
}

poller_class = None

if platform.isLinux():
    poller_class = Epoll

if platform.isWindows() or poller_class is None:
    poller_class = Select
