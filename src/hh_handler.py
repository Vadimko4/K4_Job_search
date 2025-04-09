"""модуль с классом для работы с API HH"""

from src.base_hh_handler import BaseHhHandler


class HhHandler(BaseHhHandler):

    def __init__(self):
        """конструктор класса"""
        pass

    def api_connections(self):
        """метод подключения к API"""
        pass

    def get_vacancies(self, search_query):
        """Получение вакансий, содержащих search_query, с hh.ru в формате JSON"""
        pass
