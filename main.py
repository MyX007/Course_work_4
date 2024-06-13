from src import work_with_json
from src import work_with_vacancies
from src import work_with_api

# Создание экземпляров класса и приветствие
hh_api = work_with_api.HeadHunterAPI()
py_vacs = work_with_vacancies.WorkWithVacancies
js_vacs = work_with_json.VacanciesToJSON()

print("Здравствуйте! Вы используете программу для поиска работы на сайте hh.ru")


# noinspection PyTypeChecker
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
            vac_area = str(input("Выберите страну для поиска вакансий из списка ниже (введите номер): "
                                 "\n1. Россия\n2. Беларусь\n"
                                 "3. Казахстан\n4. Узбекистан\n5. Кыргызстан\n6. Грузия\n7. Азербайджан\n"
                                 "8. Другие регионы\n0. Не имеет значения\nВведите номер страны: "))

            if vac_area == "1":
                vac_area = "113"
            elif vac_area == "2":
                vac_area = "16"
            elif vac_area == "3":
                vac_area = "40"
            elif vac_area == "4":
                vac_area = "97"
            elif vac_area == "5":
                vac_area = "48"
            elif vac_area == "6":
                vac_area = "28"
            elif vac_area == "7":
                vac_area = "9"
            elif vac_area == "8":
                vac_area = "1001"
            elif vac_area == "0" or "":
                vac_area = None

            # Получениe вакансий на основе выше перечисленных данных
            # noinspection PyTypeChecker
            hh_api_vacs = hh_api.get_vacs(vac_name, vac_only_with_salary, vac_area)

            # Сохранение вакансий в JSON файл
            js_vacs.save_vacs(hh_api_vacs)

            # Вывод полученных вакансий на экран
            for vacs in hh_api_vacs:
                print(vacs)

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
                        js_vacs.filter_by_min_salary(int(input("\nВведите минимальную зарплату: ")),
                                                     int(input("\nВведите максимальное количесвто вакансий: ")))
                        continue
                    elif sort_vacs == "2":
                        # Сортировка вакансий по убыванию максимальной зарплаты и вывод топ-N вакансий на экран
                        js_vacs.filter_by_max_salary(int(input("\nВведите минимальную зарплату: ")),
                                                     int(input("\nВведите максимальное количесвто вакансий: ")))
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
                    js_vacs.filter_by_salary_range(str(input("Введите диапозон зарплаты через дефис ("
                                                             "прим. 50000-100000)")),
                                                   int(input("\nВведите максимальное количесвто вакансий: ")))
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
                js_vacs.filter_by_keyword(input("Введите ключевое слово: "),
                                          int(input("\nВведите максимальное количесвто вакансий: ")),
                                          js_vacs.find_vacs_by_keyword_in_name)
                continue
            elif filter_funcs == "3":
                # Фильтрует вакансии по ключевым словам в описании
                js_vacs.filter_by_keyword(input("Введите ключевое слово: "),
                                          int(input("\nВведите максимальное количесвто вакансий: ")),
                                          js_vacs.find_vacs_by_keyword_in_description)
                continue
            elif filter_funcs == "4":
                # Фильтрует вакансии по ключевым словам в требованиях
                js_vacs.filter_by_keyword(input("Введите ключевое слово: "),
                                          int(input("\nВведите максимальное количесвто вакансий: ")),
                                          js_vacs.find_vacs_by_keyword_in_requirements)
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
            js_vacs.load_vacs()
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
