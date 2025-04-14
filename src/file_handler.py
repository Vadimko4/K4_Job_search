"""модуль для класса, работающего с файлами"""
import json

from src.base_classes import BaseFileHandler


class JSONSaver(BaseFileHandler):
    """класс для работы с файлами вакансий - считывания, записи"""

    def add_vacancy(self, new_vacancy):
        """добавляем новую вакансию в файл, но только в том случае, если её там нет"""
        with open(self.__file_name, encoding='utf-8') as file:
            old_vacancies = json.load(file)
        new_vacancy_data = new_vacancy.vacancy_to_dict()
        for vac in old_vacancies:
            if new_vacancy_data['vacancy_link'] == vac['alternate_url']:
                return
        old_vacancies.append(new_vacancy_data)

        with open(self.__file_name, 'a', encoding='utf-8') as file:
            json.load(old_vacancies, file)

    def add_vacancies(self, new_vacancies_list):
        """добавляем в файл список новых вакансий, только те, которых в файле нет - без дублей"""
        #  переводим список объектов-вакансий в список словарей
        new_vacancies_dict_list = [vac.vacancy_to_dict() for vac in new_vacancies_list]

        with open(self.__file_name, encoding='utf-8') as file:
            old_vacancies = json.load(file)

        for new_vac in new_vacancies_dict_list:
            if all(new_vac['vacancy_link'] != old_vac['alternate_url'] for old_vac in old_vacancies):
                old_vacancies.append(new_vac)

        with open(self.__file_name, 'a', encoding='utf-8') as file:
            json.load(old_vacancies, file)
