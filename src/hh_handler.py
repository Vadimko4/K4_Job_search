"""Модуль с классом для работы с API HH"""

import requests

from src.base_classes import BaseHhHandler


class ApiError(Exception):
    pass


class NotFoundError(ApiError):
    pass


class ServerError(ApiError):
    pass


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

    def get_vacancies(self, search_query: str):
        """Получение вакансий, содержащих search_query, с hh.ru в формате JSON"""
        self.params['text'] = search_query
        while self.params.get('page') != 20:
            response = requests.get(self.url, headers=self.headers, params=self.params)
            status_code = response.status_code
            if 300 > status_code >= 200:
                vacancies = response.json()['items']
                self.vacancies.extend(vacancies)
                self.params['page'] += 1
            elif 500 > status_code >= 400:
                raise NotFoundError("Запрос содержит ошибку или неверные данные")
            elif 600 > status_code >= 500:
                raise ServerError("На стороне сервера произошла ошибка при обработке запроса")

    def erase_old_vacancies(self):
        """Стирает ранее найденные вакансии для нового поиска"""
        self.vacancies = []
        self.params['page'] = 0
