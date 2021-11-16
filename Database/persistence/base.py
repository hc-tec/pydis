
from abc import abstractmethod


class BasePersistence:

    def __init__(self, save_file_path):
        self.save_file_path = save_file_path

    @abstractmethod
    def save(self, server):
        pass

    @abstractmethod
    def load(self):
        pass

    def create_temp_file(self):
        pass

    def remove_temp_file(self):
        pass

