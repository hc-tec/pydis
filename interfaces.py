
from abc import ABCMeta, abstractmethod


class Factory(metaclass=ABCMeta):

    @abstractmethod
    def build(self, *args, **kwargs):
        ...


class IEnable(metaclass=ABCMeta):

    @abstractmethod
    def is_enable(self):
        ...

    @abstractmethod
    def enable(self):
        ...

    @abstractmethod
    def disabled(self):
        ...


class IBufferManager(metaclass=ABCMeta):

    @abstractmethod
    def get_buffer(self):
        ...

    @abstractmethod
    def append_to_buffer(self, data):
        ...

    @abstractmethod
    def clear_buffer(self):
        ...
