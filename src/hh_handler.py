"""модуль с классом для работы с API HH"""

import requests

from src.base_hh_handler import BaseHhHandler


class HhHandler(BaseHhHandler):
    """
    Класс для работы с API HeadHunter
    """

    def __init__(self, file_handler):
        """конструктор класса"""
        self.url = 'https://api.hh.ru/vacancies'
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'text': '', 'page': 0, 'per_page': 200}
        self.vacancies = []
        super().__init__(file_handler)

    def get_vacancies(self, search_query):
        """Получение вакансий, содержащих search_query, с hh.ru в формате JSON"""
        self.params['text'] = search_query
        while self.params.get('page') != 20:
            response = requests.get(self.url, headers=self.headers, params=self.params)
            vacancies = response.json()['items']
            self.vacancies.extend(vacancies)
            self.params['page'] += 1
