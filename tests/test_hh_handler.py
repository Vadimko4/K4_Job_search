import json
from unittest.mock import patch

import pytest

from src.hh_handler import NotFoundError, ServerError


def test_hh_handler_init(test_hh_handler_object):
    assert test_hh_handler_object.url == 'https://api.hh.ru/vacancies'
    assert test_hh_handler_object.headers == {'User-Agent': 'HH-User-Agent'}
    assert test_hh_handler_object.params == {'text': '', 'page': 0, 'per_page': 100}
    assert test_hh_handler_object.vacancies == []


@patch('requests.get')
def test_get_vacancies_with_not_found_error(mock_get, test_hh_handler_object):
    mock_get.return_value.status_code = 400
    with pytest.raises(NotFoundError):
        test_hh_handler_object.get_vacancies('python')


@patch('requests.get')
def test_get_vacancies_with_servererror(mock_get, test_hh_handler_object):
    mock_get.return_value.status_code = 500
    with pytest.raises(ServerError):
        test_hh_handler_object.get_vacancies('python')


@patch('requests.get')
def test_get_vacancies(mock_get, test_hh_handler_object):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "items": [
            {
                "name": "Python-разработчик",
                "alternate_url": "https://hh.ru/vacancy/118870179",
                "salary": {"from": 40000, "to": 80000, "currency": "RUR", "gross": False},
                "snippet": {"requirement": "Опыт разработки на Python с Django"}
            }
        ] * 100  # 100 вакансий
    }
    test_hh_handler_object.get_vacancies('python')
    assert test_hh_handler_object.vacancies == [
            {
                "name": "Python-разработчик",
                "alternate_url": "https://hh.ru/vacancy/118870179",
                "salary": {"from": 40000, "to": 80000, "currency": "RUR", "gross": False},
                "snippet": {"requirement": "Опыт разработки на Python с Django"}
            }
        ] * 2000


def test_erase_old_vacancies(test_hh_handler_object, test_hh_json_answer):
    test_hh_handler_object.vacancies = json.loads(test_hh_json_answer)
    test_hh_handler_object.erase_old_vacancies()
    assert len(test_hh_handler_object.vacancies) == 0
