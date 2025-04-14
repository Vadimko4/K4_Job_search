"""модуль для класса, работающего с вакансиями"""


class Vacancy:
    """
    класс, определяющий вакансии
    название вакансии, ссылка на вакансию, зарплата, краткое описание или требования
    """

    __slots__ = ('vacancy_name', 'salary_from', 'salary_to', 'vacancy_description', 'vacancy_link')

    def __init__(self, vacancy_name, vacancy_link, salary_from, salary_to, vacancy_description):
        """конструктор вакансии"""
        self.vacancy_name = vacancy_name
        self.vacancy_link = vacancy_link
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.vacancy_description = self.__validate_description(vacancy_description)

    def __validate_description(self, text):
        if text:
            return text
        else:
            return "описание не указано"

    def __str__(self):
        if not self.salary_from:
            salary_from_string = "- не указана"
        else:
            salary_from_string = str(self.salary_from)
        if not self.salary_to:
            salary_to_string = "- не указана"
        else:
            salary_to_string = str(self.salary_to)

        return (f"{self.vacancy_name}: зарплата от {salary_from_string}, до {salary_to_string}; "
                f"{self.vacancy_description}; {self.vacancy_link}")

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

    @classmethod
    def cast_vacancies_to_object_list(cls, dict_vacancies_list):
        """Преобразование набора данных из JSON ответа в список объектов"""
        instances = []
        for vacancy in dict_vacancies_list:
            name = vacancy['name']
            link = vacancy['alternate_url']
            salary_info = vacancy['salary']
            if not salary_info:
                salary_from = 0
                salary_to = 0
            else:
                if vacancy['salary']['from'] is None:
                    salary_from = 0
                else:
                    salary_from = vacancy['salary']['from']
                if vacancy['salary']['to'] is None:
                    salary_to = 0
                else:
                    salary_to = vacancy['salary']['to']
            description = vacancy['snippet']['requirement']
            instance = cls(name, link, salary_from, salary_to, description)
            instances.append(instance)
        return instances

    def vacancy_to_dict(self):
        """возвращает вакансию в виде словаря"""
        vacancy_dict = dict()
        vacancy_dict['vacancy_name'] = self.vacancy_name
        vacancy_dict['salary_from'] = self.salary_from
        vacancy_dict['salary_to'] = self.salary_to
        vacancy_dict['vacancy_description'] = self.vacancy_description
        vacancy_dict['vacancy_link'] = self.vacancy_link
        return vacancy_dict

    # def __gt__(self, other):
    #     """метод определяет больше self, чем other или нет"""
    #     pass
    #
    # def __eq__(self, other):
    #     """метод определяет равны ли self и other между собой"""
    #     pass
