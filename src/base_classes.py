"""модуль с абстрактными классами"""

from abc import ABC, abstractmethod


class BaseHhHandler(ABC):
    """
    абстрактный класс для работы с API hh.ru
    """

    @abstractmethod
    def get_vacancies(self, *args, **kwargs):
        """метод получения вакансий"""
        pass


class BaseFileHandler(ABC):
    """абстрактный класс для работы с файлами"""

    @abstractmethod
    def read_vacancies(self):
        """считывает вакансии из файла"""
        pass

    @abstractmethod
    def add_vacancy(self, *args, **kwargs):
        """добавляет вакансию в файл"""
        pass

    @abstractmethod
    def add_vacancies(self, *args, **kwargs):
        """добавляет вакансии в файл"""
        pass

    @abstractmethod
    def delete_vacancy(self, *args, **kwargs):
        """удаляет вакансию из файла"""
        pass

    @abstractmethod
    def select_from_vacancies(self, *args, **kwargs):
        """делает выборку вакансий из файла"""
        pass
