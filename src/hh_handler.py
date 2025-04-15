"""Модуль с классом для работы с API HH"""

import requests

from src.base_classes import BaseHhHandler


class HhHandler(BaseHhHandler):
    """
    Класс для работы с API HeadHunter
    """

    def __init__(self):
        """Конструктор класса"""
        self.url = 'https://api.hh.ru/vacancies'
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'text': '', 'page': 0, 'per_page': 100}
        self.vacancies = []
        # super().__init__(file_handler)

    def get_vacancies(self, search_query):
        """Получение вакансий, содержащих search_query, с hh.ru в формате JSON"""
        self.params['text'] = search_query
        while self.params.get('page') != 20:
            response = requests.get(self.url, headers=self.headers, params=self.params)
            vacancies = response.json()['items']
            self.vacancies.extend(vacancies)
            self.params['page'] += 1

    def erase_old_vacancies(self):
        """Стирает ранее найденные вакансии для нового поиска"""
        self.vacancies = []
        self.params['page'] = 0
