from abc import ABC, abstractmethod


class BaseFileHandler(ABC):
    """абстрактный класс для работы с файлами"""

    @abstractmethod
    def __init__(self, *args, **kwargs):
        """конструктор"""
        pass

    @abstractmethod
    def read_filedata(self):
        """метод получения данных из файла"""
        pass

    @abstractmethod
    def append_filedata(self):
        """метод добавления данных в файл"""
        pass

    @abstractmethod
    def clear_filedata(self):
        """метод удаления данных из файла"""
        pass
