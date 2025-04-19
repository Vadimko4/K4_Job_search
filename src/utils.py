from src.vacancy import Vacancy

VACANCY_PER_PAGE_OUT = 5


def filter_vacancies_by_words(vacancies: list[Vacancy], filter_words: list[str]) -> list[Vacancy]:
    """Фильтрует список вакансий по поисковым словам - список строк"""
    filtered_vacancies = [vac for vac in vacancies
                          if any(word in vac.vacancy_description.lower() for word in filter_words)]
    return filtered_vacancies


def is_salary_in_search_range(salary_range: tuple, vac_salary_from: int, vac_salary_to: int) -> bool:
    """Возвращает True, если диапазон зарплат вакансии соответствует поисковому диапазону"""
    if not vac_salary_to:
        return vac_salary_from >= salary_range[0] and vac_salary_from <= salary_range[1]
    elif not vac_salary_from:
        return salary_range[0] <= vac_salary_to <= salary_range[1]
    elif vac_salary_from and vac_salary_to:
        return salary_range[0] <= vac_salary_from and vac_salary_to <= salary_range[1]


def get_vacancies_by_salary(vacancies: list[Vacancy], salary_range: tuple) -> list[Vacancy]:
    """
    Фильтрует вакансии по зарплатам
    salary_range - список из двух целых чисел: зарплата от и зарплата до
    если хотя бы одно из них попадает в диапазон зарплат, указанный в вакансии от и до,
    то вакансия попадает в выдачу
    """
    filtered_vacancies = [vac for vac in vacancies
                          if is_salary_in_search_range(salary_range, vac.salary_from, vac.salary_to)]
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


# if __name__  == "__main__":
#     vac1 = Vacancy(
#         vacancy_name="Senior Продуктовый аналитик",
#         salary_from=0,
#         salary_to=550000,
#         vacancy_description="Будет плюсом, если хорошо знаешь <highlighttext>Python</highlighttext>
#         и Jupyter Notebook,"
#                             " знаком с ML, или имеешь опыт в роли инженера данных и...",
#         vacancy_link="https://hh.ru/vacancy/118511005"
#     )
#     vac2 = Vacancy(
#         vacancy_name="Системный администратор",
#         salary_from=0,
#         salary_to=530000,
#         vacancy_description="Qemu KVM. Web сервер(LAMP). Nextcloud. Mysql-Maria BD. Маршрутизация. Bash. SAMBA. "
#                             "Lets Encrypt.",
#         vacancy_link="https://hh.ru/vacancy/118268364"
#     )
#     vac3 = Vacancy(
#         vacancy_name="Lead QA",
#         salary_from=400000,
#         salary_to=500000,
#         vacancy_description="Опыт автоматизированного и нагрузочного тестирования (Selenium, JMeter, Postman) и "
#                             "работы с языками программирования
#                             (<highlighttext>Python</highlighttext>/Java/JavaScript)."
#                             " Работа с CI/CD...",
#         vacancy_link="https://hh.ru/vacancy/119356360"
#     )
#     vac4 = Vacancy(
#         vacancy_name="Ведущий backend разработчик-исследователь в Мастерскую стартапов",
#         salary_from=300000,
#         salary_to=0,
#         vacancy_description="описание не указано",
#         vacancy_link="https://hh.ru/vacancy/119356360"
#     )
#     obj_vacancies = [vac1, vac2, vac3, vac4]
#     sorted_vac = sort_vacancies_by_salary_decrease(obj_vacancies)
#     for i in sorted_vac:
#         print (i.vacancy_name)
