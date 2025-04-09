from abc import ABC, abstractmethod


class BaseHhHandler(ABC):
    """
    абстрактный класс для работы с API hh.ru
    """

    @abstractmethod
    def __init__(self, *args, **kwargs):
        """конструктор"""
        pass

    @abstractmethod
    def get_vacancies(self, *args, **kwargs):
        """метод получения вакансий"""
        pass
