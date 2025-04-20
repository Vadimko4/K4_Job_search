import pytest

from src.vacancy import Vacancy
from src.hh_handler import HhHandler
from src.file_handler import JSONSaver

@pytest.fixture()
def test_json_saver_object():
    return JSONSaver()


@pytest.fixture()
def test_hh_handler_object():
    return HhHandler()


@pytest.fixture()
def test_obj_vacancy_list(first_test_vacancy, second_test_vacancy,  third_test_vacancy, fourth_test_vacancy):
    return [first_test_vacancy, second_test_vacancy, third_test_vacancy, fourth_test_vacancy]


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


@pytest.fixture()
def fourth_test_vacancy():
    return Vacancy(
        vacancy_name="Ведущий backend разработчик-исследователь в Мастерскую стартапов",
        salary_from=300000,
        salary_to=0,
        vacancy_description="описание не указано",
        vacancy_link="https://hh.ru/vacancy/119356360"
    )


@pytest.fixture()
def none_description_test_vacancy():
    return Vacancy(
        vacancy_name="Ведущий backend разработчик-исследователь в Мастерскую стартапов",
        salary_from=300000,
        salary_to=0,
        vacancy_description="",
        vacancy_link="https://hh.ru/vacancy/119356360"
    )


@pytest.fixture()
def test_hh_json_answer():
    return ('[{"name":"Python-разработчик","alternate_url":"https://hh.ru/vacancy/118870179","salary":'
            '{"from":40000,"to":80000,"currency":"RUR","gross":false},"snippet":'
            '{"requirement":"Инициативность в поиске решения задач. '
            'Опыт разработки на языке \u003Chighlighttext\u003EPython\u003C/highlighttext\u003E с фреймворком Django. '
            'Понимание принципов ООП и SOLID. "}},{"name":"Junior Python Developer",'
            '"alternate_url":"https://hh.ru/vacancy/118941947","salary":{"from":130000,"to":300000,"currency":"RUR",'
            '"gross":true},"snippet":{"requirement":"Знания \u003Chighlighttext\u003EPython\u003C/highlighttext\u003E '
            'на базовом уровне. Опыт работы с фреймворками Flask или Django (будет плюсом). Опыт работы с реляционными '
            'базами данных..."}},{"name":"Python-разработчик","alternate_url":"https://hh.ru/vacancy/119691755",'
            '"salary":{"from":50000,"to":null,"currency":"RUR","gross":true},"snippet":'
            '{"requirement":"Понимание концепции асинхронного программирования '
            'в \u003Chighlighttext\u003EPython\u003C/highlighttext\u003E. - Опыт работы с FastAPI, Pydantic, '
            'Pytest,\u003Chighlighttext\u003Epython\u003C/highlighttext\u003E-telegram-bot/aiogram, SQLAlchemy, '
            'alembic. - "}},{"name":"Junior+/Middle Backend Developer (Python, FastAPI, PostgreSQL)","alternate_url":'
            '"https://hh.ru/vacancy/119610326","salary":null,"snippet":{"requirement":"Коммерческий опыт '
            'разработки на \u003Chighlighttext\u003EPython\u003C/highlighttext\u003E от 1 года. '
            'Знание фреймворка FastAPI. Понимание принципов работы реляционных баз данных и владение SQL. "}},'
            '{"name":"Python разработчик", "alternate_url":"https://hh.ru/vacancy/119687981","salary":'
            '{"from":400,"to":1000,"currency":"USD","gross":false},"snippet":{"requirement":'
            '"Знание языка \u003Chighlighttext\u003Epython\u003C/highlighttext\u003E. Знание хотя бы одного фреймворка '
            'для backend разработки: django, flask, fastapi - обязательно. Знание архитектурных паттернов. "}}]')
