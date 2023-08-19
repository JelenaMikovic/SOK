from abc import ABC, abstractmethod


class ServiceBase(ABC):
    @abstractmethod
    def identifier(self):
        pass

    @abstractmethod
    def name(self):
        pass


class Visualization(ServiceBase):

    @abstractmethod
    def display(self,graph):
        pass


class Parser(ServiceBase):

    @abstractmethod
    def load(self, file_path):
        pass
