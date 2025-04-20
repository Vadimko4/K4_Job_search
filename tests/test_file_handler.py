from src.file_handler import DEFAULT_VACANCY_JSON_FILE_NAME


def test_json_saver_init(test_json_saver_object):
    assert test_json_saver_object.get_filename() == DEFAULT_VACANCY_JSON_FILE_NAME
