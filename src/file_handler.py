"""модуль для класса, работающего с файлами"""
import json
import os

from src.base_classes import BaseFileHandler

PATH_TO_VACANCY_JSON_FILE = os.path.join(os.path.dirname(__file__), '..', "data", "vacancy.json")


class JSONSaver(BaseFileHandler):
    """класс для работы с файлами вакансий - считывания, записи"""

    def __init__(self, file_name=PATH_TO_VACANCY_JSON_FILE):
        """конструктор"""
        self.__file_name = file_name

    def read_filedata(self) -> list[dict]:
        """считывает и возвращает данные - список словарей с вакансиями из json файла"""
        with open(self.__file_name, encoding='utf-8') as file:
            return json.load(file)

    def append_filedata(self, add_data: list[dict]):
        """дописываем данные в json файл"""
        with open(self.__file_name, 'a', encoding='utf-8') as file:
            json.dump(add_data, file)

    def delete_filedata(self, vacancy):
        """удаляем вакансию из файла, если она там есть"""
        dict_vacancy = vacancy.vacancy_to_dict()
        vacancies = self.read_filedata()
        if dict_vacancy in vacancies:
            vacancies.remove(dict_vacancy)

        with open(self.__file_name, 'w', encoding='utf-8') as file:
            json.dump(vacancies, file)

    def add_vacancy(self, new_vacancy):
        """добавляем новую вакансию в файл, но только в том случае, если её там нет"""
        old_vacancies = self.read_filedata()
        new_vacancy_data = new_vacancy.vacancy_to_dict()

        for vac in old_vacancies:
            if new_vacancy_data['vacancy_link'] == vac['alternate_url']:
                return

        old_vacancies.append(new_vacancy_data)
        self.append_filedata(old_vacancies)

    def add_vacancies(self, new_vacancies_list):
        """добавляем в файл новые вакансии, только те, которых в файле нет - без дублей"""
        #  переводим список объектов-вакансий в список словарей
        new_vacancies_dict_list = [vac.vacancy_to_dict() for vac in new_vacancies_list]

        old_vacancies = self.read_filedata()

        for new_vac in new_vacancies_dict_list:
            if all(new_vac['vacancy_link'] != old_vac['alternate_url'] for old_vac in old_vacancies):
                old_vacancies.append(new_vac)

        self.append_filedata(old_vacancies)
