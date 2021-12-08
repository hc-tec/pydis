
from typing import List
from abc import abstractmethod


class AbstractObserver:

    @abstractmethod
    def update(self, *args, **kwargs): ...


class AbstractSubject:

    @abstractmethod
    def attach(self, observer: AbstractObserver): ...

    @abstractmethod
    def detach(self, observer: AbstractObserver): ...

    @abstractmethod
    def notify(self, *args, **kwargs): ...


class Observer(AbstractObserver):

    def update(self, *args, **kwargs):
        pass


class Subject(AbstractSubject):

    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self, *args, **kwargs):
        for observer in self._observers:
            observer.update(*args, **kwargs)
