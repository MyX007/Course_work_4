import json
from abc import ABC, abstractmethod


class VacsToJSONAbs(ABC):
    """
    Абстрактный класс для работы с json файлом с вакансиями
    """
    @staticmethod
    @abstractmethod
    def save_vacs(self):
        pass

    @classmethod
    @abstractmethod
    def find_vacs_by_keyword_in_name(cls, key):
        pass

    @classmethod
    @abstractmethod
    def find_vacs_by_keyword_in_requirements(cls, key):
        pass

    @classmethod
    @abstractmethod
    def find_vacs_by_keyword_in_description(cls, key):
        pass

    @staticmethod
    @abstractmethod
    def delete_vac(key):
        pass

    @staticmethod
    @abstractmethod
    def filter_by_min_salary(min_salary, quantity_vacs):
        pass

    @staticmethod
    @abstractmethod
    def filter_by_max_salary(max_salary, quantity_vacs):
        pass

    @staticmethod
    @abstractmethod
    def filter_by_salary_range(salary_range, top_vacs):
        pass

    @staticmethod
    @abstractmethod
    def load_vacs():
        pass

    @staticmethod
    @abstractmethod
    def clear_file():
        pass


class VacanciesToJSON(VacsToJSONAbs):
    """
    Класс для работы с json файлом с вакансиями
    """
    @staticmethod
    def save_vacs(vacs_list):
        """
        Метод для сохранения вакансий в json файл
        """
        with open("src/vacancies.json", "w", encoding="UTF-8") as file:
            json.dump([vac for vac in vacs_list], file,
                      indent=4, ensure_ascii=False, sort_keys=False)

    @classmethod
    def find_vacs_by_keyword_in_name(cls, key):
        """
        Метод для пойска ключевых слов в названии вакансии
        """
        sorted_vacs = []
        with open("src/vacancies.json", "r", encoding="UTF-8") as file:
            vacancies = json.load(file)

            for item in vacancies:
                if key.lower() in item["name"].lower():
                    sorted_vacs.append(item)
            return sorted_vacs

    @classmethod
    def find_vacs_by_keyword_in_requirements(cls, key):
        """
        Метод для пойска ключевых слов в требованиях к вакансии
        """
        sorted_vacs = []
        with open("src/vacancies.json", "r", encoding="UTF-8") as file:
            vacancies = json.load(file)

            for item in vacancies:
                if key.lower() in item["requirements"].lower():
                    sorted_vacs.append(item)
            return sorted_vacs

    @classmethod
    def find_vacs_by_keyword_in_description(cls, key):
        """
        Метод для пойска ключевых слов в описании вакансии
        """
        sorted_vacs = []
        with open("src/vacancies.json", "r", encoding="UTF-8") as file:
            vacancies = json.load(file)

            for item in vacancies:
                if key.lower() in item["description"].lower():
                    sorted_vacs.append(item)
            return sorted_vacs

    @staticmethod
    def delete_vac(key):
        """
        Метод для удаления вакансии из файла по номеру id
        """

        with open("src/vacancies.json", "r", encoding="UTF-8") as file:
            vacancies = json.load(file)

        for item in vacancies:
            if key in item["id"]:
                vacancies.remove(item)

        with open("src/vacancies.json", "w", encoding="UTF-8") as file:
            json.dump(vacancies, file, indent=4, ensure_ascii=False, sort_keys=False)

    @staticmethod
    def filter_by_min_salary(min_salary, quantity_vacs):
        """
        Метод для фильрации вакансий по минимальной зарплате.
        Получает на вход параметры минимальной зарплаты(min_salary) и максимальное количество вакансий,
        которые нужно вывести на экран(quantity_vacs)
        """

        with open("src/vacancies.json", "r", encoding="UTF-8") as file:
            vacancies = json.load(file)
            filtred_salary = []

            for salary in vacancies:
                if salary["salary min"] >= min_salary:
                    filtred_salary.append(salary)
            sorted_vacs = sorted(filtred_salary, key=lambda x: x.get("salary min", ""), reverse=False)

            return sorted_vacs

    @staticmethod
    def filter_by_max_salary(max_salary, quantity_vacs):

        """
        Метод для фильрации вакансий по максимальной зарплате.
        Получает на вход параметры максимальной зарплаты(max_salary) и максимальное количество вакансий,
        которые нужно вывести на экран(quantity_vacs)
        """

        with open("src/vacancies.json", "r", encoding="UTF-8") as file:
            vacancies = json.load(file)
            filtred_salary = []

            for salary in vacancies:
                if salary["salary max"] <= max_salary:
                    filtred_salary.append(salary)

            sorted_vacs = sorted(filtred_salary, key=lambda x: x.get("salary max", ""), reverse=True)

            return sorted_vacs

    @staticmethod
    def filter_by_salary_range(salary_range, top_vacs):
        """
        Метод для фильтрации вакансий по диапозону зарплат
        """
        salary_range_split = salary_range.split("-")

        with open("src/vacancies.json", "r", encoding="UTF-8") as file:
            vacancies = json.load(file)
            filtred_salary = []

            for salary in vacancies:
                if salary["salary min"] >= int(salary_range_split[0]) and salary["salary max"] <= int(
                        salary_range_split[1]):
                    filtred_salary.append(salary)
            sorted_vacs = sorted(filtred_salary, key=lambda x: x.get("salary min", ""), reverse=False)

            return sorted_vacs

    @staticmethod
    def load_vacs():
        """
        Метод для вывода вакансий из json файла на экран
        """
        with open("src/vacancies.json", "r", encoding="UTF-8") as file:
            vacancies = json.load(file)

            return vacancies

    @staticmethod
    def clear_file():
        """
        Метод для очистки файла с вакансиями
        """
        with open("src/vacancies.json", "w", encoding="UTF-8"):
            pass
