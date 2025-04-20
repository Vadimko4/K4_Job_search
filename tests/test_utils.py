import pytest

from src.utils import (filter_vacancies_by_words, get_top_vacancies, get_vacancies_by_salary,
                       is_salary_in_search_range, sort_vacancies_by_salary_decrease)


def test_filter_vacancies_by_words(test_obj_vacancy_list):
    filtered_vacancies = filter_vacancies_by_words(test_obj_vacancy_list, 'маршрутизация'.split())
    assert len(filtered_vacancies) == 1
    assert filtered_vacancies[0].vacancy_name == 'Системный администратор'
    assert filtered_vacancies[0].salary_from == 0
    assert filtered_vacancies[0].salary_to == 530000
    assert filtered_vacancies[0].vacancy_description == ("Qemu KVM. Web сервер(LAMP). Nextcloud. Mysql-Maria BD. "
                                                         "Маршрутизация. Bash. SAMBA. Lets Encrypt.")
    assert filtered_vacancies[0].vacancy_link == 'https://hh.ru/vacancy/118268364'
    filtered_vacancies = filter_vacancies_by_words(test_obj_vacancy_list, 'abracadabra'.split())
    assert len(filtered_vacancies) == 0


@pytest.mark.parametrize('salary_range, vac_salary_from, vac_salary_to, expected',
                         [((300, 500), 0, 400, True),
                          ((300, 500), 400, 0, True),
                          ((300, 500), 100, 200, False),
                          ((300, 500), 600, 700, False),
                          ((0, 500), 100, 400, True),
                          ((0, 500), 600, 0, False),
                          ((0, 500), 0, 400, True)])
def test_is_salary_in_search_range(salary_range, vac_salary_from, vac_salary_to, expected):
    assert is_salary_in_search_range(salary_range, vac_salary_from, vac_salary_to) == expected


def test_get_vacancies_by_salary(test_obj_vacancy_list):
    filtered_vacancy = get_vacancies_by_salary(test_obj_vacancy_list, (300000, 350000))
    assert len(filtered_vacancy) == 1
    assert filtered_vacancy[0].vacancy_name == "Ведущий backend разработчик-исследователь в Мастерскую стартапов"
    assert filtered_vacancy[0].salary_from == 300000
    assert filtered_vacancy[0].salary_to == 0
    assert filtered_vacancy[0].vacancy_description == "описание не указано"
    assert filtered_vacancy[0].vacancy_link == "https://hh.ru/vacancy/119356360"


def test_sort_vacancies_by_salary_decrease(test_obj_vacancy_list):
    sorted_vacancies = sort_vacancies_by_salary_decrease(test_obj_vacancy_list)
    assert sorted_vacancies[0].vacancy_name == "Senior Продуктовый аналитик"
    assert sorted_vacancies[1].vacancy_name == "Системный администратор"
    assert sorted_vacancies[2].vacancy_name == "Lead QA"
    assert sorted_vacancies[3].vacancy_name == "Ведущий backend разработчик-исследователь в Мастерскую стартапов"


def test_get_top_vacancies(test_obj_vacancy_list):
    top_vacancies = get_top_vacancies(test_obj_vacancy_list, 3)
    assert len(top_vacancies) == 3
    assert top_vacancies[0].vacancy_name == "Senior Продуктовый аналитик"
    assert top_vacancies[1].vacancy_name == "Системный администратор"
    assert top_vacancies[2].vacancy_name == "Lead QA"
