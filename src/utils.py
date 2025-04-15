from src.vacancy import Vacancy

VACANCY_PER_PAGE_OUT = 5


def filter_vacancies_by_words(vacancies: list[Vacancy], filter_words: list[str]) -> list[Vacancy]:
    """Фильтрует список вакансий по поисковым словам - список строк"""
    filtered_vacancies = [vac for vac in vacancies
                          if any(word in vac.vacancy_description.lower() for word in filter_words)]
    return filtered_vacancies


def get_vacancies_by_salary(vacancies: list[Vacancy], salary_range: tuple) -> list[Vacancy]:
    """
    Фильтрует вакансии по зарплатам
    salary_range - список из двух целых чисел: зарплата от и зарплата до
    если хотя бы одно из них попадает в диапазон зарплат, указанный в вакансии от и до,
    то вакансия попадает в выдачу
    """
    filtered_vacancies = [vac for vac in vacancies
                          if any(amount in range(vac.salary_to, vac.salary_from + 1)
                                 for amount in salary_range)]
    return filtered_vacancies


def sort_vacancies_by_salary_decrease(vacancies: list[Vacancy]) -> list[Vacancy]:
    """Сортирует вакансии по убыванию актуальной зарплаты"""
    return sorted(vacancies, reverse=True)


def get_top_vacancies(vacancies: list[Vacancy], top_amount: int) -> list[Vacancy]:
    """Возвращает топ n вакансий"""
    top_vacancies = vacancies[:top_amount]
    return top_vacancies


def print_vacancies(vacancies: list[Vacancy]) -> None:
    """Выводит список вакансий в удобном для чтения виде"""
    cnt = 0
    for vac in vacancies:
        print(vac)
        cnt += 1
        if cnt % VACANCY_PER_PAGE_OUT == 0:
            user_input = input("<q> - возврат в главное меню, остальное - продолжить вывод: ").lower()
            if user_input == 'q':
                return
