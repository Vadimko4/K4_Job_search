import os
from typing import Any
import datetime
from src.file_handler import JSONSaver, DEFAULT_VACANCY_JSON_FILE_NAME, PATH_TO_DATA_DIR
from src.hh_handler import HhHandler, NotFoundError, ServerError
from src.vacancy import Vacancy
from src.utils import (print_vacancies, get_vacancies_by_salary, sort_vacancies_by_salary_decrease,
                       filter_vacancies_by_words, get_top_vacancies)


def user_menu_out():
    """Функция выводит главное меню программы"""
    print("\nВыберите дальнейшее действие")
    print("""\n1. Фильтрация по зарплате
2. Фильтрация по ключевым словам в описании
3. Вывести ТОП найденных вакансий по зарплате
4. Вывести все вакансии
5. Действия с файлом
6. Сбросить все фильтры
7. Новый поиск
8. Ещё раз показать главное меню
9. Выход из программы""")


def user_file_menu_out():
    """Функция выводит меню для работы с файлами"""
    print("\nВыберите дальнейшее действие")
    print("""\n1. Записать текущие вакансии в файл
2. Загрузить вакансии из файла
3. Вернуться в главное меню""")


def foolproof_user_menu_input(menu_range_input: list[str]) -> str:
    """
    Функция выбора пользователя пункта меню - принимает от пользователя только
    цифры, которые содержатся в menu_range_input
    """
    while True:
        user_answer = input('\nПользователь: ')
        if len(user_answer) != 1 or user_answer not in menu_range_input:
            print(f"\nПрограмма: Неверный ввод, вам нужно ввести значение от {menu_range_input[0]} "
                  f"до {menu_range_input[-1]} \nПопробуйте ещё раз")
        else:
            break
    return user_answer


def foolproof_user_salary_input():
    """Ввод пользователя уровня зарплаты для фильтрации вакансий"""
    while True:
        print("\nПрограмма: введите интересующий уровень зарплаты в одном из форматов: \n"
              "<100000 - 500000> = от 100.000 руб до 500.000 руб \n"
              "<100000> = от 100.000 руб\n"
              "<-500000> = до 500.000 руб")
        user_answer = input('\nПользователь: ')
        if (any(char not in '0123456789- ' for char in user_answer)
                or user_answer.count('-') > 1 or user_answer[-1] == '-'):
            print("\nПрограмма: Неверный ввод. Попробуйте ещё раз")
        else:
            user_answer = user_answer.strip()
            salary = user_answer.split('-')
            if user_answer[0] == '-':
                salary_to = int(salary[1])
                salary_from = 0
            elif len(salary) == 2:
                salary_from, salary_to = map(int, salary)
                if salary_from > salary_to:
                    print("\nПрограмма: Неверный ввод. Попробуйте ещё раз")
                    continue
            else:
                salary_from = int(salary[0])
                salary_to = 10 ** 10
            break
    return salary_from, salary_to


def foolproof_user_top_amount_input(n_max: int) -> int:
    """Функция ввода количества вакансий для вывода ТОП вакансий по зарплате"""
    print(f"\nПрограмма: введите количество вакансий в ТОП: число от 1 до {n_max}")
    while True:
        try:
            user_answer = int(input('Пользователь: '))
            if user_answer not in range(1, n_max + 1):
                raise ValueError
        except ValueError:
            print(f"\nПрограмма: Неверный ввод, вам нужно ввести число от 1 до {n_max} \nПопробуйте ещё раз")
        except Exception:
            print(f"\nПрограмма: Неверный ввод, вам нужно ввести число  \nПопробуйте ещё раз")
        else:
            break
    return user_answer


def create_new_file_object(old_file_object=None) -> tuple:
    """
    Функция инициирует создание нового файлового объекта класса JSONSaver
    запрашивает у пользователя имя нового файла предлагает варианты
    если файл с таким именем уже существует, спрашивает перезаписать его или изменить имя
    """
    today = datetime.datetime.today()
    day = today.day
    month = today.month
    year = today.year

    new_file_object = old_file_object
    file_mode = None
    quit_flag = False

    while not quit_flag:
        print(f"\nПрограмма: введите имя нового файла (без расширения имени). \n"
              f"Можете в нём использовать текущую дату: {day}_{month}_{year}\n"
              f"При нажатии ENTER - будет использовано по умолчанию имя vacancy.json")
        file_name = input("\nПользователь: ")
        if not file_name:
            new_file_name = DEFAULT_VACANCY_JSON_FILE_NAME
        else:
            if file_name[-5:] != '.json':
                file_name = file_name + '.json'
            new_file_name = os.path.join(PATH_TO_DATA_DIR, file_name)
        #  Проверяем, есть ли файл с таким именем
        try:  # файл с таким именем уже существует
            with open(new_file_name, 'r', encoding='utf-8') as file:
                pass
            print(f"\nПрограмма: файл с таким именем уже существует\n"
                  f"0 - вернуться в меню действий с файлом\n"
                  f"1 - ввести другое имя файла\n"
                  f"2 - перезаписать данные поверх\n"
                  f"3 - добавить данные в файл")
            user_answer = foolproof_user_menu_input(list('0123'))
            if user_answer == '0':  # новый файловый объект не создаётся, возвращаемся в меню файл
                quit_flag = True
            elif user_answer == '2':  # открываем файл для перезаписи
                file_mode = 'rewrite'
            elif user_answer == '3':  # дописать новые данные
                file_mode = 'append'
        except FileNotFoundError:  # файла с таким именем нет, создаём и выходим
            with open(new_file_name, 'w', encoding='utf-8'):
                pass
            new_file_object = JSONSaver(new_file_name)
            file_mode = 'new'
            quit_flag = True

    return new_file_object, file_mode


def create_open_file_object() -> Any:
    """
    Функция делает попытку открыть существующий файл и создать связанный с ним объект класса JSONSaver
    выводит список существующих файлов
    если существующих файлов нет, то возвращает None
    в случае успеха - вернёт новый файловый объект
    """
    # Получаем список файлов и папок в текущей директории
    files = os.listdir(PATH_TO_DATA_DIR)

    # Выводим только файлы
    print("\nПрограмма: читаю список файлов\n")
    files_list = []
    for item in files:
        full_path = os.path.join(PATH_TO_DATA_DIR, item)  # Формируем полный путь
        if os.path.isfile(full_path):
            files_list.append(item)
            print(f"{len(files_list)}: {item}")
    if not files_list:
        print("\nПрограмма: в директории нет файлов\n")
        return None
    else:
        print("\nПрограмма: введите номер файла, который нужно открыть")
        user_answer = foolproof_user_menu_input(list(map(str, range(1, len(files_list) + 1))))
        full_file_name = os.path.join(PATH_TO_DATA_DIR, files_list[int(user_answer) - 1])
        return JSONSaver(full_file_name)


def file_user_menu(vacancies: list[Vacancy], file_object: JSONSaver = None) -> tuple:
    """
    Функция обеспечивает исполнение файлового меню пользователя
    в случае открытия нового файла возвращает новый файловый объект, новый список вакансий и флаг изменения
    первичного (нефильтрованного) списка вакансий
    Здесь пользователь может:
    1 - Записать текущие данные в файл
    (если в настоящий момент файл не выбран, то программа предлагает открыть существующий файл - для добавления
    информации, либо перезаписи, или же создать новый файл
    если файл выбран, то предлагает создать новый файл, добавить данные в старый или же перезаписать его)
    2 - Загрузить данные о вакансиях из файла
    3 - Вернуться в главное меню
    """
    new_vacancies = vacancies
    new_file_object = file_object
    is_primary_vacancies_update = False
    file_quit_flag = False

    while not file_quit_flag:
        print(f"\nПрограмма: В настоящий момент в списке {len(new_vacancies)} вакансий.")
        user_file_menu_out()
        user_input = foolproof_user_menu_input(list('123'))

        if user_input == '1':  # Записать текущие данные в файл
            if new_file_object is not None:  # если файл уже открыт
                if new_file_object.is_empty:  # и если он пустой
                    new_file_object.add_vacancies(new_vacancies)
                    print("\nПрограмма: новые вакансии успешно добавлены в файл")
                else:  # если он не пустой
                    print("\nПрограмма: текущий файл не пустой. Выберите вариант действий:\n"
                          "0 - вернуться в файловое меню\n"
                          "1 - записать данные в новый файл\n"
                          "2 - записать новые данные поверх старых\n"
                          "3 - дописать новые данные\n"
                          "4 - открыть другой файл и записать новые данные поверх старых\n"
                          "5 - открыть другой файл и дописать новые данные")
                    user_input_1 = foolproof_user_menu_input(list('012345'))

                    if user_input_1 == '1':  # записать данные в новый файл
                        next_file_object, file_mode = create_new_file_object(new_file_object)
                        if next_file_object != new_file_object:
                            new_file_object = next_file_object
                            if file_mode in ('new', 'rewrite'):
                                new_file_object.rewrite_vacancy(new_vacancies)
                                if file_mode == 'new':
                                    print("\nПрограмма: новые вакансии успешно добавлены в новый файл")
                                else:
                                    print("\nПрограмма: новые вакансии перезаписаны в файл поверх старых")
                            elif file_mode == 'append':
                                new_file_object.add_vacancies(new_vacancies)
                                print("\nПрограмма: новые вакансии успешно добавлены в файл")
                        else:
                            print("\nПрограмма: вакансии не добавлены в файл, попробуйте ещё раз")
                    elif user_input_1 == '2':  # записать новые данные поверх старых
                        new_file_object.rewrite_vacancy(new_vacancies)
                        print("\nПрограмма: новые вакансии успешно записаны в файл поверх старых")
                    elif user_input_1 == '3':  # дописать новые данные
                        new_file_object.add_vacancies(new_vacancies)
                        print("\nПрограмма: новые вакансии успешно добавлены в файл")
                        new_vacancies = Vacancy.cast_vacancies_to_object_list(new_file_object.read_vacancies())
                        new_vacancies = sort_vacancies_by_salary_decrease(new_vacancies)
                    elif user_input_1 == '4':  # открыть существующий файл и записать новые данные поверх старых
                        new_file_object = create_open_file_object()
                        if new_file_object is not None:
                            new_file_object.rewrite_vacancy(new_vacancies)
                            print("\nПрограмма: новые вакансии успешно записаны в файл поверх старых")
                        else:
                            print("\nПрограмма: не удалось открыть файл, "
                                  "вакансии не были добавлены, попробуйте ещё раз")
                    elif user_input_1 == '5':  # открыть существующий файл и дописать новые данные
                        new_file_object = create_open_file_object()
                        if new_file_object is not None:
                            new_file_object.add_vacancies(new_vacancies)
                            new_vacancies = Vacancy.cast_vacancies_to_object_list(new_file_object.read_vacancies())
                            new_vacancies = sort_vacancies_by_salary_decrease(new_vacancies)
                            print("\nПрограмма: новые вакансии успешно добавлены в файл")
                        else:
                            print("\nПрограмма: не удалось открыть файл, "
                                  "вакансии не были добавлены, попробуйте ещё раз")

            else:  # если файл ещё не открыт, то надо открыть существующий или создать новый
                print("\nПрограмма: в настоящий момент нет открытого файла. Что вы хотите:\n\n"
                      "0 - вернуться в файловое меню\n"
                      "1 - создать новый файл\n"
                      "2 - открыть существующий файл и записать новые данные поверх старых\n"
                      "3 - открыть существующий файл и дописать новые данные")
                user_input_1 = foolproof_user_menu_input(list('0123'))

                if user_input_1 == '1':  # создать новый файл
                    create_file_object, file_mode = create_new_file_object()
                    if create_file_object is not None:
                        new_file_object = create_file_object
                        if file_mode in ('new', 'rewrite'):
                            new_file_object.rewrite_vacancy(new_vacancies)
                            if file_mode == 'new':
                                print("\nПрограмма: новые вакансии успешно добавлены в новый файл")
                            else:
                                print("\nПрограмма: новые вакансии перезаписаны в файл поверх старых")
                        elif file_mode == 'append':
                            new_file_object.add_vacancies(new_vacancies)
                            print("\nПрограмма: новые вакансии успешно добавлены в файл")
                    else:
                        print("\nПрограмма: не удалось создать файл, вакансии не были добавлены, попробуйте ещё раз")

                if user_input_1 == '2':  # открыть существующий файл и записать новые данные поверх старых
                    open_file_object = create_open_file_object()
                    if open_file_object is None:  # файл открыть не получилось, так как в папке data нет файлов
                        print("\nПрограмма: не удалось открыть файл, вакансии не добавлены, попробуйте ещё раз")
                    else:
                        new_file_object = open_file_object
                        new_file_object.rewrite_vacancy(new_vacancies)
                        print("\nПрограмма: новые вакансии успешно добавлены в файл поверх старых")

                if user_input_1 == '3':  # открыть существующий файл и дописать новые данные
                    open_file_object = create_open_file_object()
                    if open_file_object is None:  # файл открыть не получилось, так как в папке data нет файлов
                        print("\nПрограмма: не удалось открыть файл, вакансии не добавлены, попробуйте ещё раз")
                    else:
                        new_file_object = open_file_object
                        new_file_object.add_vacancies(new_vacancies)
                        new_vacancies = Vacancy.cast_vacancies_to_object_list(new_file_object.read_vacancies())
                        new_vacancies = sort_vacancies_by_salary_decrease(new_vacancies)
                        print("\nПрограмма: новые вакансии успешно добавлены в файл")

        if user_input == '2':  # Загрузить данные о вакансиях из файла
            print("\nПрограмма: внимание, при успешном открытии и чтении файла, "
                  "первичные данные поиска будут больше не доступны!")
            open_file_object = create_open_file_object()
            if open_file_object is None:  # файл открыть не получилось, так как в папке data нет файлов
                print("\nПрограмма: не удалось открыть файл, вакансии не добавлены, попробуйте ещё раз")
            else:
                new_file_object = open_file_object
                #  Считываем вакансии из файла, как список словарей и преобразуем в список объектов
                new_vacancies = Vacancy.cast_vacancies_to_object_list(new_file_object.read_vacancies())
                is_primary_vacancies_update = True
                print("\nПрограмма: вакансии успешно считаны из файла")

        if user_input == '3':  # Вернуться в главное меню
            file_quit_flag = True

    return new_vacancies, new_file_object, is_primary_vacancies_update


def user_interaction():
    """Основная функция реализует интерфейс пользователя и программы"""
    is_file_open = False
    #  В самом начале никакой файл не открыт и объекта класса JSONSaver не существует
    file_object = None
    # Создание экземпляра класса для работы с API сайтов с вакансиями
    hh_api = HhHandler()

    # platforms = ["HeadHunter"]
    search_query = input("Программа: Введите ключевое слово для поиска вакансий. \n\nПользователь: ")
    print("\nПрограмма: подождите, идёт сбор данных c www.hh.ru...")
    #  при получении пустого ответа - ошибка возникает!!!
    try:
        hh_api.get_vacancies(search_query)
    except NotFoundError:
        print("\nПрограмма: Запрос содержит ошибку или неверные данные, вакансии не были получены")
    except ServerError:
        print("\nПрограмма: На стороне сервера произошла ошибка при обработке запроса, вакансии не были получены")
    if hh_api.vacancies:
        vacancies = Vacancy.cast_hh_vacancies_to_object_list(hh_api.vacancies)
    else:
        vacancies = []
    primary_vacancies = vacancies
    print("\nДанные успешно получены")

    quit_flag = False
    while not quit_flag:
        print(f"\nПрограмма: В настоящий момент в списке {len(vacancies)} вакансий.")
        user_menu_out()

        user_input = foolproof_user_menu_input(list('123456789'))
        if user_input == '1':  # Фильтрация по зарплате
            salary_from, salary_to = foolproof_user_salary_input()
            vacancies = get_vacancies_by_salary(vacancies, (salary_from, salary_to))
            vacancies = sort_vacancies_by_salary_decrease(vacancies)

        if user_input == '2':  # Фильтрация по ключевым словам в описании
            print("\nПрограмма: через пробел введите ключевые слова для поиска в описании вакансии")
            user_answer = input('Пользователь: ').lower()
            filter_words = user_answer.split()
            vacancies = filter_vacancies_by_words(vacancies, filter_words)

        if user_input == '3':  # Вывести ТОП найденных вакансий по зарплате
            top_amount = foolproof_user_top_amount_input(len(vacancies))
            vacancies = sort_vacancies_by_salary_decrease(vacancies)
            top_vacancies = get_top_vacancies(vacancies, top_amount)
            print_vacancies(top_vacancies)

        if user_input == '4':  # Вывести все вакансии
            print_vacancies(vacancies)

        if user_input == '5':  # Действия с файлом
            vacancies, file_object, is_primary_vacancies_update = file_user_menu(vacancies, file_object)
            if is_primary_vacancies_update:
                primary_vacancies = vacancies

        if user_input == '6':  # Сбросить все фильтры
            vacancies = primary_vacancies

        if user_input == '7':  # Новый поиск
            hh_api.erase_old_vacancies()
            search_query = input("\nПрограмма: Введите ключевое слово для поиска вакансий. \n\nПользователь: ")
            print("\nПрограмма: подождите, идёт сбор данных c www.hh.ru...")
            hh_api.get_vacancies(search_query)
            vacancies = Vacancy.cast_hh_vacancies_to_object_list(hh_api.vacancies)
            print("\nДанные успешно получены")

        if user_input == '8':  # Ещё раз показать главное меню
            user_menu_out()

        if user_input == '9':  # Выход из программы
            print("\nПрограмма: Всего доброго!")
            quit_flag = True


if __name__ == "__main__":
    user_interaction()
