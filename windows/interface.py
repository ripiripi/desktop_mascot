from abc import ABC, abstractmethod


class Subject(ABC):
    def __init__(self):
        self.observers = []

    @abstractmethod
    def add_observer(self, observer):
        self.observers.append(observer)

    @abstractmethod
    def notify_observers(self, event):
        for observer in self.observers:
            observer.update(event)


class Observer(ABC):
    @abstractmethod
    def update(self, event):
        raise NotImplementedError("Subclass must implement 'update' method")
