
from typing import List
from abc import abstractmethod


class AbstractObserver:

    @abstractmethod
    def update(self, subject): ...


class AbstractSubject:

    @abstractmethod
    def attach(self, observer: AbstractObserver): ...

    @abstractmethod
    def detach(self, observer: AbstractObserver): ...

    @abstractmethod
    def notify(self): ...


class Observer(AbstractObserver):

    def update(self, subject: AbstractSubject):
        pass


class Subject(AbstractSubject):

    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update(self)
