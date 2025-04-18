import pytest

from src.vacancy import Vacancy


def test_vacancy_init(first_test_vacancy, second_test_vacancy):
    assert first_test_vacancy.vacancy_name == "Senior Продуктовый аналитик"
    assert first_test_vacancy.salary_from == 0
    assert first_test_vacancy.salary_to == 550000
    assert first_test_vacancy.vacancy_description == ("Будет плюсом, если хорошо знаешь "
                                                      "<highlighttext>Python</highlighttext> и Jupyter Notebook, "
                                                      "знаком с ML, или имеешь опыт в роли инженера данных и...")
    assert first_test_vacancy.vacancy_link == "https://hh.ru/vacancy/118511005"

    assert second_test_vacancy.vacancy_name == "Системный администратор"
    assert second_test_vacancy.salary_from == 0
    assert second_test_vacancy.salary_to == 530000
    assert second_test_vacancy.vacancy_description == ("Qemu KVM. Web сервер(LAMP). Nextcloud. Mysql-Maria BD. "
                                                       "Маршрутизация. Bash. SAMBA. Lets Encrypt.")
    assert second_test_vacancy.vacancy_link == "https://hh.ru/vacancy/118268364"
