"""Модуль с абстрактными классами"""

from abc import ABC, abstractmethod


class BaseHhHandler(ABC):
    """
    Абстрактный класс для работы с API hh.ru
    """

    @abstractmethod
    def get_vacancies(self, *args, **kwargs):
        """Метод получения вакансий"""
        pass


class BaseFileHandler(ABC):
    """Абстрактный класс для работы с файлами"""

    @abstractmethod
    def read_vacancies(self):
        """Считывает вакансии из файла"""
        pass

    @abstractmethod
    def add_vacancy(self, *args, **kwargs):
        """Добавляет вакансию в файл"""
        pass

    @abstractmethod
    def add_vacancies(self, *args, **kwargs):
        """Добавляет вакансии в файл"""
        pass

    @abstractmethod
    def rewrite_vacancy(self,  *args, **kwargs):
        """Перезаписывает вакансии в файл - старые стирает"""
        pass

    @abstractmethod
    def delete_vacancy(self, *args, **kwargs):
        """Удаляет вакансию из файла"""
        pass

    @abstractmethod
    def select_from_vacancies(self, *args, **kwargs):
        """Делает выборку вакансий из файла"""
        pass
