from src.hh_handler import HhHandler


def test_hh_handler_init(test_hh_handler_object):
    assert test_hh_handler_object.url == 'https://api.hh.ru/vacancies'
    assert test_hh_handler_object.headers == {'User-Agent': 'HH-User-Agent'}
    assert test_hh_handler_object.params == {'text': '', 'page': 0, 'per_page': 100}
    assert test_hh_handler_object.vacancies == []
