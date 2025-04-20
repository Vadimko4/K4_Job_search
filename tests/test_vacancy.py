import json

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


def test_vacancy_validate_description(second_test_vacancy, none_description_test_vacancy):
    assert (second_test_vacancy._Vacancy__validate_description(second_test_vacancy.vacancy_description) ==
            "Qemu KVM. Web сервер(LAMP). Nextcloud. Mysql-Maria BD. Маршрутизация. Bash. SAMBA. Lets Encrypt.")
    assert (none_description_test_vacancy._Vacancy__validate_description
            (none_description_test_vacancy.vacancy_description) == "описание не указано")


def test_vacancy_str(second_test_vacancy, third_test_vacancy, fourth_test_vacancy):
    assert str(second_test_vacancy) == (f"{'-' * 150}\nВакансия: Системный администратор \nЗарплата: до 530000 рублей"
                                        f"\nОписание: Qemu KVM. Web сервер(LAMP). Nextcloud. Mysql-Maria BD. "
                                        f"Маршрутизация. Bash. SAMBA. Lets Encrypt.\nСсылка на вакансию: "
                                        f"https://hh.ru/vacancy/118268364")

    assert str(third_test_vacancy) == (f"{'-' * 150}\nВакансия: Lead QA \nЗарплата: от 400000 - до 500000 рублей\n"
                                       f"Описание: Опыт автоматизированного и нагрузочного тестирования (Selenium, "
                                       f"JMeter, Postman) и работы с языками программирования "
                                       f"(<highlighttext>Python</highlighttext>/Java/JavaScript). Работа с CI/CD...\n"
                                       f"Ссылка на вакансию: https://hh.ru/vacancy/119356360")

    assert (str(fourth_test_vacancy) ==
            (f"{'-' * 150}\nВакансия: Ведущий backend разработчик-исследователь в Мастерскую стартапов \n"
             f"Зарплата: от 300000 рублей\nОписание: описание не указано\nСсылка на вакансию: "
             f"https://hh.ru/vacancy/119356360"))


def test_vacancy_lt(first_test_vacancy, second_test_vacancy, third_test_vacancy, fourth_test_vacancy):
    condition = (first_test_vacancy > second_test_vacancy)
    assert condition is True
    condition = (second_test_vacancy > third_test_vacancy)
    assert condition is True
    condition = (third_test_vacancy > fourth_test_vacancy)
    assert condition is True
    condition = (first_test_vacancy < fourth_test_vacancy)
    assert condition is False
    condition = (first_test_vacancy == first_test_vacancy)
    assert condition is True


def test_vacancy_cast_hh_vacancies_to_object_list(test_hh_json_answer):
    dict_vacancies_list = json.loads(test_hh_json_answer)
    obj_vacancies_list = Vacancy.cast_hh_vacancies_to_object_list(dict_vacancies_list)
    assert obj_vacancies_list[0].vacancy_name == "Python-разработчик"
    assert obj_vacancies_list[0].salary_from == 40000
    assert obj_vacancies_list[0].salary_to == 80000
    assert (obj_vacancies_list[0].vacancy_description ==
            "Инициативность в поиске решения задач. Опыт разработки на языке "
            "\u003Chighlighttext\u003EPython\u003C/highlighttext\u003E с фреймворком Django. "
            "Понимание принципов ООП и SOLID. ")
    assert obj_vacancies_list[0].vacancy_link == "https://hh.ru/vacancy/118870179"

    assert obj_vacancies_list[3].vacancy_name == "Junior+/Middle Backend Developer (Python, FastAPI, PostgreSQL)"
    assert obj_vacancies_list[3].salary_from == 0
    assert obj_vacancies_list[3].salary_to == 0
    assert (obj_vacancies_list[3].vacancy_description ==
            "Коммерческий опыт разработки на \u003Chighlighttext\u003EPython\u003C/highlighttext\u003E от 1 года. "
            "Знание фреймворка FastAPI. Понимание принципов работы реляционных баз данных и владение SQL. ")
    assert obj_vacancies_list[3].vacancy_link == "https://hh.ru/vacancy/119610326"


def test_vacancy_cast_vacancies_to_object_list(first_test_vacancy, second_test_vacancy):
    dict_vacancies_list = [first_test_vacancy.vacancy_to_dict(), second_test_vacancy.vacancy_to_dict()]
    obj_vacancies_list = Vacancy.cast_vacancies_to_object_list(dict_vacancies_list)
    assert obj_vacancies_list[0].vacancy_name == "Senior Продуктовый аналитик"
    assert obj_vacancies_list[0].salary_from == 0
    assert obj_vacancies_list[0].salary_to == 550000
    assert (obj_vacancies_list[0].vacancy_description ==
            ("Будет плюсом, если хорошо знаешь <highlighttext>Python</highlighttext> и Jupyter Notebook, "
             "знаком с ML, или имеешь опыт в роли инженера данных и..."))
    assert obj_vacancies_list[0].vacancy_link == "https://hh.ru/vacancy/118511005"

    assert obj_vacancies_list[1].vacancy_name == "Системный администратор"
    assert obj_vacancies_list[1].salary_from == 0
    assert obj_vacancies_list[1].salary_to == 530000
    assert (obj_vacancies_list[1].vacancy_description ==
            "Qemu KVM. Web сервер(LAMP). Nextcloud. Mysql-Maria BD. Маршрутизация. Bash. SAMBA. Lets Encrypt.")
    assert obj_vacancies_list[1].vacancy_link == "https://hh.ru/vacancy/118268364"


def test_vacancy_to_dict(first_test_vacancy, fourth_test_vacancy):
    assert (first_test_vacancy.vacancy_to_dict() ==
            {'vacancy_name': 'Senior Продуктовый аналитик',
             'salary_from': 0, 'salary_to': 550000,
             'vacancy_description': 'Будет плюсом, если хорошо знаешь <highlighttext>Python</highlighttext> и Jupyter '
                                    'Notebook, знаком с ML, или имеешь опыт в роли инженера данных и...',
             'vacancy_link': 'https://hh.ru/vacancy/118511005'})

    assert (fourth_test_vacancy.vacancy_to_dict() ==
            {'vacancy_name': 'Ведущий backend разработчик-исследователь в Мастерскую стартапов',
             'salary_from': 300000, 'salary_to': 0, 'vacancy_description': 'описание не указано',
             'vacancy_link': 'https://hh.ru/vacancy/119356360'})
