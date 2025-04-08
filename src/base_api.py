from abc import ABC, abstractmethod


class BaseApi(ABC):
    """
    абстрактный класс для работы с API
    """

    @abstractmethod
    def __init__(self, *args, **kwargs):
        """конструктор"""
        pass

    @abstractmethod
    def api_connections(self):
        """метод подключения к API"""
        pass

    @abstractmethod
    def get_vacancies(self):
        """метод получения вакансий"""
        pass
