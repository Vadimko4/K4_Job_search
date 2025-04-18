import pytest

from src.vacancy import Vacancy

@pytest.fixture()
def first_test_vacancy():
    return Vacancy(
        vacancy_name="Senior Продуктовый аналитик",
        salary_from=0,
        salary_to=550000,
        vacancy_description="Будет плюсом, если хорошо знаешь <highlighttext>Python</highlighttext> и Jupyter Notebook,"
                            " знаком с ML, или имеешь опыт в роли инженера данных и...",
        vacancy_link="https://hh.ru/vacancy/118511005"
    )


@pytest.fixture()
def second_test_vacancy():
    return Vacancy(
        vacancy_name="Системный администратор",
        salary_from=0,
        salary_to=530000,
        vacancy_description="Qemu KVM. Web сервер(LAMP). Nextcloud. Mysql-Maria BD. Маршрутизация. Bash. SAMBA. "
                            "Lets Encrypt.",
        vacancy_link="https://hh.ru/vacancy/118268364"
    )


@pytest.fixture()
def third_test_vacancy():
    return Vacancy(
        vacancy_name="Lead QA",
        salary_from=400000,
        salary_to=500000,
        vacancy_description="Опыт автоматизированного и нагрузочного тестирования (Selenium, JMeter, Postman) и "
                            "работы с языками программирования (<highlighttext>Python</highlighttext>/Java/JavaScript)."
                            " Работа с CI/CD...",
        vacancy_link="https://hh.ru/vacancy/119356360"
    )
