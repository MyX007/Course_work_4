from src.work_with_api import HeadHunterAPI
from src.work_with_vacancies import Vacancies
from src.work_with_json import VacanciesToJSON
from data.config import area

# Создание экземпляров класса и приветствие
hh_api = HeadHunterAPI()
py_vacs = Vacancies
js_vacs = VacanciesToJSON

print("Здравствуйте! Вы используете программу для поиска работы на сайте hh.ru")


def create_vacs(vacs_list):
    created_vacs = []
    for vac in vacs_list:
        vacs = py_vacs(vac["name"],
                       vac["employer"]["name"],
                       vac["alternate_url"],
                       vac["published_at"],
                       (vac.get('salary', {}) or {}).get('from', 0),
                       (vac.get('salary', {}) or {}).get('to', 0),
                       (vac.get('salary', {}) or {}).get('currency', 0),
                       vac["area"]["name"],
                       vac["snippet"]["responsibility"],
                       vac["id"],
                       vac["snippet"]["requirement"])
        created_vacs.append(vacs.format_to_save_in_json())
    return created_vacs


def print_vacs(vac_list, max_vacs=100):
    for vac in vac_list[:max_vacs]:
        print(py_vacs(vac["name"],
                      vac["employer"],
                      vac["link"],
                      vac["published_at"],
                      vac["salary min"],
                      vac["salary max"],
                      vac["currency"],
                      vac["locality"],
                      vac["description"],
                      vac["id"],
                      vac["requirements"]))


def get_area(user_area: str) -> str:
    return area.get(user_area)


def main_func():
    """
    Функция интерактива с пользователем
    """
    while True:
        # Выбор основных действий для работы с программой
        functions = input("\nВыберите действие (введите номер):\n1. Искать вакансии \n2. Отфильтровать вакансии\n"
                          "3. Удалить вакансию из списка\n4. Показать сохраненные вакансии\n"
                          "5. Очистить файл с вакансиями\n0. Завершить программу\n-> ")

        if functions == "1":
            # Ввод названия нужной вакансии
            vac_name = str(input("Введите название вакансии: "))
            if vac_name == "":
                print("Нельзя ввести пустое имя! Начните заново.")
                continue

            # Сортировка вакансий по наличию зарплаты
            vac_only_with_salary = str(input("Показывать вакансии без указанной зарплаты?(да/нет): ").lower())

            if vac_only_with_salary == "да":
                vac_only_with_salary = False
            else:
                vac_only_with_salary = True

            # Выбор страны для поиска вакансий
            user_area = str(input("Выберите страну для поиска вакансий из списка ниже (введите номер): "
                                  "\n1. Россия\n2. Беларусь\n"
                                  "3. Казахстан\n4. Узбекистан\n5. Кыргызстан\n6. Грузия\n7. Азербайджан\n"
                                  "8. Другие регионы\n0. Не имеет значения\nВведите номер страны: "))

            if user_area in area.keys():
                vac_area = get_area(user_area)

            else:
                vac_area = None

            # Получениe вакансий на основе выше перечисленных данных
            # noinspection PyTypeChecker
            hh_api_vacs = hh_api.get_vacs(vac_name, vac_only_with_salary, vac_area)

            vacs_list = []

            for vac in hh_api_vacs:
                vacs_list.append(vac)

            # Сохранение вакансий в JSON файл
            js_vacs.save_vacs(create_vacs(vacs_list))

            # Вывод полученных вакансий на экран
            print_vacs(create_vacs(vacs_list))

            continue
        if functions == "2":

            # Выбор действий по сортировке вакансий
            filter_funcs = str(input("\nВыберите действие (введите номер): \n1. Фильтровать по зарплате\n"
                                     "2. Фильтровать по ключевым словам в названии \n"
                                     "3. Фильтровать по ключевым словам в описании\n"
                                     "4. Фильтровать по ключевым словам в требованиях\n"
                                     "0. Вернуться в начало\n-> "))

            if filter_funcs == "1":
                # Выбор действий по сортировке вакансий по зарплате
                filter_salary = str(input("\nВыберите действие (введите номер):"
                                          "\n1. Фильтровать по зарплате\n"
                                          "2. Фильтровать по диапозону зарплат\n"
                                          "0. Вернуться в начало\n-> "))

                if filter_salary == "1":

                    # Выбор действий по сортировке вакансий по зарплате
                    sort_vacs = str(input("\nВыберите действие (введите номер):"
                                          "\n1. Сортировка по возрастанию минимальной зарплаты\n"
                                          "2. Сортировка по убыванию максимальной\n"
                                          "0. Вернуться в начало\n-> "))

                    if sort_vacs == "1":
                        # Сортировка вакансий по возрастанию минимальной зарплаты и вывод N количества вакансий на экран
                        min_salary = int(input("\nВведите минимальную зарплату: "))
                        max_vacs = int(input("\nВведите максимальное количесвто вакансий: "))
                        filtred_vacs = js_vacs.filter_by_min_salary(min_salary, max_vacs)
                        print_vacs(filtred_vacs, max_vacs)
                        continue
                    elif sort_vacs == "2":
                        # Сортировка вакансий по убыванию максимальной зарплаты и вывод топ-N вакансий на экран
                        max_salary = int(input("\nВведите минимальную зарплату: "))
                        max_vacs = int(input("\nВведите максимальное количесвто вакансий: "))
                        js_vacs.filter_by_max_salary(max_salary, max_vacs)
                        continue

                    elif sort_vacs == "0":
                        # Возврат в начало программы
                        continue

                    else:
                        # В случае, если введено значение, не совпадающее с пунктами программы,
                        # возвращает пользователся к началу программы
                        print("Введено неверное значение! Начните заново.")
                        continue

                elif filter_salary == "2":
                    # Фильтрует вакансии по диапозону зарплаты (min-max)
                    salary_range = str(input("Введите диапозон зарплаты через дефис (прим. 50000-100000)"))
                    max_vacs = int(input("\nВведите максимальное количесвто вакансий: "))
                    js_vacs.filter_by_salary_range(salary_range, max_vacs)

                    continue

                elif filter_salary == "0":
                    # Возвращает пользователся к началу программы
                    continue

                else:
                    # В случае, если введено значение, не совпадающее с пунктами программы,
                    # возвращает пользователся к началу программы
                    print("Введено неверное значение! Начните заново.")
                    continue

            elif filter_funcs == "2":
                # Фильтрует вакансии по ключевым словам в названии
                key = input("Введите ключевое слово: ")
                max_vacs = int(input("\nВведите максимальное количесвто вакансий: "))

                filtred_vacs = js_vacs.find_vacs_by_keyword_in_name(key)
                print_vacs(filtred_vacs, max_vacs)

                continue
            elif filter_funcs == "3":
                # Фильтрует вакансии по ключевым словам в описании
                key = input("Введите ключевое слово: ")
                max_vacs = int(input("\nВведите максимальное количесвто вакансий: "))

                filtred_vacs = js_vacs.find_vacs_by_keyword_in_description(key)
                print_vacs(filtred_vacs, max_vacs)
                continue
            elif filter_funcs == "4":
                # Фильтрует вакансии по ключевым словам в требованиях
                key = input("Введите ключевое слово: ")
                max_vacs = int(input("\nВведите максимальное количесвто вакансий: "))

                filtred_vacs = js_vacs.find_vacs_by_keyword_in_requirements(key)
                print_vacs(filtred_vacs, max_vacs)
                continue
            elif filter_funcs == "0":
                # Возвращает пользователся к началу программы
                continue

            else:
                # В случае, если введено значение, не совпадающее с пунктами программы,
                # возвращает пользователся к началу программы
                print("Введено неверное значение! Начните заново.")
                continue
        elif functions == "3":
            # Ищет вакансию по id(получает из ввода пользователя) и удалаят ее из файла с вакансиями
            js_vacs.delete_vac(str(input("Скопируйте id нужной вакансии и вставьте сюда: ")))
            print("Вакансия удалена!")
            continue

        elif functions == "4":
            # Выводит на экран все вакансии из файла с вакансиями
            print_vacs(js_vacs.load_vacs())
            continue

        elif functions == "5":
            # Очищает файл с вакансиями
            js_vacs.clear_file()
            print("Файл очищен!")
            continue

        elif functions == "0":
            # Заваершение программы
            print("Программа успешно завершена!")
            break

        else:
            # В случае, если введено значение, не совпадающее с пунктами программы,
            # возвращает пользователся к началу программы
            print("Введено неверное значение! Начните заново.")
            continue


if __name__ == "__main__":
    main_func()
