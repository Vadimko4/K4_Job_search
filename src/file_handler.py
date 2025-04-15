"""Модуль для класса, работающего с файлами"""
import json
import os

from src.base_classes import BaseFileHandler

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
            json.dump(vacancies, file)

    def rewrite_vacancy(self, new_vacancies):
        """Перезаписывает вакансии в файл - старые стирает"""
        with open(self.__file_name, 'w', encoding='utf-8') as file:
            json.dump(new_vacancies, file)

    def add_vacancy(self, new_vacancy):
        """Добавляем новую вакансию в файл, но только в том случае, если её там нет"""
        old_vacancies = self.read_vacancies()
        new_vacancy_data = new_vacancy.vacancy_to_dict()

        for vac in old_vacancies:
            if new_vacancy_data['vacancy_link'] == vac['alternate_url']:
                return

        old_vacancies.append(new_vacancy_data)

        with open(self.__file_name, 'a', encoding='utf-8') as file:
            json.dump(old_vacancies, file)

    def add_vacancies(self, new_vacancies_list):
        """Добавляем в файл новые вакансии, только те, которых в файле нет - без дублей"""
        #  переводим список объектов-вакансий в список словарей
        new_vacancies_dict_list = [vac.vacancy_to_dict() for vac in new_vacancies_list]

        old_vacancies = self.read_vacancies()

        for new_vac in new_vacancies_dict_list:
            if all(new_vac['vacancy_link'] != old_vac['alternate_url'] for old_vac in old_vacancies):
                old_vacancies.append(new_vac)

        with open(self.__file_name, 'a', encoding='utf-8') as file:
            json.dump(old_vacancies, file)

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


if __name__ == '__main__':
    files = os.listdir('.')
    print(files[1])
    # Выводим только файлы
    files_count = 0
    for item in files:
        if os.path.isfile(item):
            files_count += 1
            print(f"{files_count}: {item}")
