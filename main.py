from src.file_handler import JSONSaver
from src.hh_handler import HhHandler
from src.vacancy import Vacancy
from src.utils import (print_vacancies, get_vacancies_by_salary, sort_vacancies_by_salary_decrease,
                       filter_vacancies_by_words, get_top_vacancies)


def user_menu_out():
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


def foolproof_user_menu_input() -> str:
    """
    Функция выбора пользователя пункта главного меню - цифры от 1 до 8
    """
    while True:
        user_answer = input('\nПользователь: ')
        if len(user_answer) != 1 or user_answer not in '123456789':
            print("\nПрограмма: Неверный ввод, вам нужно ввести цифру от 1 - до 9 \nПопробуйте ещё раз")
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
            salary = user_answer.split('-')
            if user_answer[0] == '-':
                salary_to = int(salary[0])
                salary_from = 0
            elif len(salary) == 2:
                salary_from, salary_to = map(int, salary)
                if salary_from > salary_to:
                    print("\nПрограмма: Неверный ввод. Попробуйте ещё раз")
                    continue
            else:
                salary_from = int(salary[0])
                salary_to = 10**8
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


# Получение вакансий с hh.ru в формате JSON
# hh_vacancies = hh_api.get_vacancies("Python")
#
# # Преобразование набора данных из JSON в список объектов
# vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)
#
# # Пример работы контструктора класса с одной вакансией
# vacancy = Vacancy("Python Developer", "<https://hh.ru/vacancy/123456>", "100 000-150 000 руб.", "Требования: опыт работы от 3 лет...")
#
# # Сохранение информации о вакансиях в файл
# json_saver = JSONSaver()
# json_saver.add_vacancy(vacancy)
# json_saver.delete_vacancy(vacancy)

# Функция для взаимодействия с пользователем


def user_interaction():
    # Создание экземпляра класса для работы с json-файлом с вакансиями
    # json_saver = JSONSaver()
    # Создание экземпляра класса для работы с API сайтов с вакансиями
    hh_api = HhHandler()

    # platforms = ["HeadHunter"]
    search_query = input("Программа: Введите ключевое слово для поиска вакансий. \n\nПользователь: ")
    print("\nПрограмма: подождите, идёт сбор данных...")
    hh_api.get_vacancies(search_query)
    vacancies = Vacancy.cast_vacancies_to_object_list(hh_api.vacancies)
    print("\nДанные с www.hh.ru успешно получены")

    quit_flag = False
    while not quit_flag:
        print(f"\nПрограмма: В настоящий момент в списке {len(vacancies)} вакансий.")
        user_menu_out()

        user_input = foolproof_user_menu_input()
        if user_input == '1':
            salary_from, salary_to = foolproof_user_salary_input()
            vacancies = get_vacancies_by_salary(vacancies, (salary_from, salary_to))
            vacancies = sort_vacancies_by_salary_decrease(vacancies)

        if user_input == '2':
            print("\nПрограмма: через пробел введите ключевые слова для поиска в описании вакансии")
            user_answer = input('Пользователь: ').lower()
            filter_words = user_answer.split()
            vacancies = filter_vacancies_by_words(vacancies, filter_words)
        if user_input == '3':
            top_amount = foolproof_user_top_amount_input(len(vacancies))
            vacancies = sort_vacancies_by_salary_decrease(vacancies)
            top_vacancies = get_top_vacancies(vacancies, top_amount)
            print_vacancies(top_vacancies)
        if user_input == '4':
            print_vacancies(vacancies)
        if user_input == '5':
            pass
        if user_input == '6':
            vacancies = Vacancy.cast_vacancies_to_object_list(hh_api.vacancies)
        if user_input == '7':
            hh_api.erase_old_vacancies()
            search_query = input("\nПрограмма: Введите ключевое слово для поиска вакансий. \n\nПользователь: ")
            print("\nПрограмма: подождите, идёт сбор данных...")
            hh_api.get_vacancies(search_query)
            vacancies = Vacancy.cast_vacancies_to_object_list(hh_api.vacancies)
            print("\nДанные с www.hh.ru успешно получены")
        if user_input == '8':
            user_menu_out()
        if user_input == '9':
            print("Программа: Всего доброго!")
            exit()


    # top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    # filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    # salary_range = input("Введите диапазон зарплат: ") # Пример: 100000 - 150000
    #
    # filtered_vacancies = filter_vacancies(vacancies_list, filter_words)
    #
    # ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)
    #
    # sorted_vacancies = sort_vacancies(ranged_vacancies)
    # top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
    # print_vacancies(top_vacancies)


if __name__ == "__main__":
    user_interaction()
