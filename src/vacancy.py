"""модуль для класса, работающего с вакансиями"""


class Vacancy:
    """
    класс, определяющий вакансии
    название вакансии, ссылка на вакансию, зарплата, краткое описание или требования
    """

    def __init__(self, vacancy_name, vacancy_link, salary_from, salary_to, vacancy_desription):
        """конструктор вакансии"""
        self.vacancy_name = vacancy_name
        self.vacancy_link = vacancy_link
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.vacancy_desription = vacancy_desription

