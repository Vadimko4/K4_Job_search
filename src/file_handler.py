"""модуль для класса, работающего с файлами"""
import json

from src.base_classes import BaseFileHandler


class JSONSaver(BaseFileHandler):
    """класс для работы с файлами вакансий - считывания, записи"""

    def add_vacancy(self, vacancy):
        with open(self.__file_name, encoding='utf-8') as file:
            old_vacancies = json.load(file)
        new_vacancy_data = vacancy.vacancy_to_dict()
        for vac in old_vacancies:
            if new_vacancy_data['vacancy_link'] == vac['alternate_url']:
                return
        old_vacancies.append(new_vacancy_data)

        with open(self.__file_name, 'a', encoding='utf-8') as file:
            json.load(old_vacancies, file)
