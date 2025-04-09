from src.vacancy import Vacancy


def user_interaction():
    pass


def cast_vacancies_to_object_list(hh_vacancies) -> list[Vacancy]:
    """Преобразование набора данных из JSON в список объектов"""
    vacancies_list = []
    return vacancies_list


def filter_vacancies(vacancies, filter_words):
    """фильтрует список вакансий по поисковым словам"""
    pass


def get_vacancies_by_salary(vacancies, salary_range):
    """фильтрует вакансии по зарплатам"""
    pass


def sort_vacancies(vacancies):
    """сортирует вакансии по убыванию актуальной зарплаты"""
    return sorted(vacancies, reverse=True)


def get_top_vacancies(vacancies, top_n):
    """возвращает топ n вакансий"""
    pass


def print_vacancies(vacancies):
    """выводит список вакансий в удобном для чтения виде"""
    pass
