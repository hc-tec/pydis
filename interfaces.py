
from abc import ABCMeta, abstractmethod


class Factory(metaclass=ABCMeta):

    @abstractmethod
    def build(self, *args, **kwargs):
        pass




