"""Модуль для класса, работающего с файлами"""
import json
import os

from src.base_classes import BaseFileHandler
from src.vacancy import Vacancy

PATH_TO_DATA_DIR = os.path.join(os.path.dirname(__file__), '..', "data")
DEFAULT_VACANCY_JSON_FILE_NAME = os.path.join(PATH_TO_DATA_DIR, "vacancy.json")


class JSONSaver(BaseFileHandler):
    """Класс для работы с файлами вакансий - считывания, записи"""

    def __init__(self, file_name=DEFAULT_VACANCY_JSON_FILE_NAME):
        """Конструктор"""
        self.__file_name = file_name

    def __eq__(self, other):
        """Метод определяет равны ли self и other между собой"""
        return self.__file_name == other.__file_name

    @property
    def is_empty(self):
        """Возвращает - пустой ли файл"""
        return os.path.getsize(self.__file_name) == 0

    def read_vacancies(self) -> list[dict]:
        """Считывает и возвращает данные - список словарей с вакансиями из json файла"""
        with open(self.__file_name, encoding='utf-8') as file:
            return json.load(file)

    def delete_vacancy(self, vacancy):
        """Удаляем вакансию из файла, если она там есть"""
        dict_vacancy = vacancy.vacancy_to_dict()
        vacancies = self.read_vacancies()
        if dict_vacancy in vacancies:
            vacancies.remove(dict_vacancy)

        with open(self.__file_name, 'w', encoding='utf-8') as file:
            json.dump(vacancies, file, ensure_ascii=False, indent=4)

    def rewrite_vacancy(self, new_vacancies: list[Vacancy]):
        """Перезаписывает вакансии в файл - старые стирает"""
        new_vacancies_dict_list = [vac.vacancy_to_dict() for vac in new_vacancies]
        with open(self.__file_name, 'w', encoding='utf-8') as file:
            json.dump(new_vacancies_dict_list, file, ensure_ascii=False, indent=4)

    def add_vacancy(self, new_vacancy):
        """Добавляем новую вакансию в файл, но только в том случае, если её там нет"""
        old_vacancies = self.read_vacancies()
        new_vacancy_data = new_vacancy.vacancy_to_dict()

        for vac in old_vacancies:
            if new_vacancy_data['vacancy_link'] == vac['vacancy_link']:
                return

        old_vacancies.append(new_vacancy_data)

        with open(self.__file_name, 'a', encoding='utf-8') as file:
            json.dump(old_vacancies, file, ensure_ascii=False, indent=4)

    def add_vacancies(self, new_vacancies_list: list[Vacancy]):
        """Добавляем в файл новые вакансии, только те, которых в файле нет - без дублей"""
        #  переводим список объектов-вакансий в список словарей
        new_vacancies_dict_list = [vac.vacancy_to_dict() for vac in new_vacancies_list]

        #  Читаем вакансии,  которые уже есть в файле
        old_vacancies = self.read_vacancies()

        #  Добавляем в итоговый список только те, которых не было - новые уникальные
        for new_vac in new_vacancies_dict_list:
            if all(new_vac['vacancy_link'] != old_vac['vacancy_link'] for old_vac in old_vacancies):
                old_vacancies.append(new_vac)
        #  Перезаписываем дополненные данные вместо старых
        with open(self.__file_name, 'w', encoding='utf-8') as file:
            json.dump(old_vacancies, file, ensure_ascii=False, indent=4)

    def select_from_vacancies(self, salary_range, filter_words) -> list[dict]:
        """
        Делает выборку вакансий из файла по указанному диапазону зарплаты (список из двух целых значений: от и до)
        и по указанным ключевым словам (список строк), которые должны присутствовать (хотя бы одно из них)
        в описании вакансии
        """
        vacancies_list = self.read_vacancies()
        selected_vacancies = [vac for vac in vacancies_list
                              if any(word in vac['description'] for word in filter_words)
                              and (salary_range[0] in range(vac['salary_from'], vac['salary_to'] + 1) or
                                   salary_range[1] in range(vac['salary_from'], vac['salary_to'] + 1))]
        return selected_vacancies


# if __name__ == '__main__':
#     a = JSONSaver()
#     print(a)
#     b = a
#     print(b, a)
