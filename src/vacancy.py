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

    def __lt__(self, other):
        """
        метод определяет меньше self, чем other или нет
        сравнение производится по актуальной зарплате:
        если есть и нижний и верхний пределы, то это их среднее арифметическое
        если есть только одно из значений, то это оно
        """
        if self.salary_to and self.salary_from:  # определяем актуальную зарплату для self
            self_salary = (self.salary_to + self.salary_from) / 2
        elif self.salary_to:
            self_salary = self.salary_to
        else:
            self_salary = self.salary_from
        
        if other.salary_to and other.salary_from:  # определяем актуальную зарплату для other
            other_salary = (other.salary_to + other.salary_from) / 2
        elif other.salary_to:
            other_salary = other.salary_to
        else:
            other_salary = other.salary_from

        return self_salary < other_salary

    def __gt__(self, other):
        """метод определяет больше self, чем other или нет"""
        pass

    def __eq__(self, other):
        """метод определяет равны ли self и other между собой"""
        pass
