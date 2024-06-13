from abc import ABC, abstractmethod
import requests
import datetime


class Vacancies(ABC):
    """
    Абстрактный класс для работы с вакансиями
    """
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def __gt__(self, other):
        pass

    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def format_to_save_in_json(self):
        pass


class WorkWithVacancies(Vacancies):
    """
    Класс для работы с вакансиями
    """

    def __init__(self, name, employer, link, published_at, salary_min, salary_max, currency, locality, description,
                 id_vac, requirements):
        """
        Конструктор класса
        """
        self.name = name
        self.employer = employer
        self.link = link
        self.published_at = published_at
        self.salary_min = salary_min
        if salary_min is None:
            self.salary_min = 0
        self.salary_max = salary_max
        if salary_max is None:
            self.salary_max = 0
        self.currency = currency
        if currency is None:
            self.currency = ""
        self.locality = locality
        self.description = description
        if self.description is None:
            self.description = "Описание отсутсвуют"
        self.requirements = requirements
        if self.requirements is None:
            self.requirements = "Требования отсутсвует"
        self.id_vac = id_vac

    def __gt__(self, other):
        """
        Метод для сравнения вакансий по максимальной зарплате
        """

        if self.salary_max > other.salary_max:
            return True
        else:
            return False

    def validate(self):
        """
        Метод для форматирования атрибутов класса для дальнейшего использования в методе '__str__'
        """
        self.published_at = datetime.datetime.strptime(self.published_at[:10], "%Y-%m-%d").date()

        if self.salary_min == 0 and self.salary_max != 0:
            self.salary_min = ""
            self.salary_max = f"До {self.salary_max}"
        elif self.salary_max == 0 and self.salary_min != 0:
            self.salary_max = ""
            self.salary_min = f"От {self.salary_min}"
        elif self.salary_min == 0 and self.salary_max == 0:
            self.salary_min = "Зарплата не указана"
            self.salary_max = ""
            self.currency = ""
        else:
            self.salary_min = f"От {self.salary_min}"
            self.salary_max = f"До {self.salary_max}"

    def __str__(self):
        """
        Метод для вывода информации об экземпляре класса на экран пользователя

        """
        WorkWithVacancies.validate(self)
        return (f"\nВакансия: {self.name}\nЗарплата: {self.salary_min} {self.salary_max} {self.currency}\n"
                f"Работодатель: {self.employer}\nОпубликовано: {self.published_at}\nНаселенный пункт: {self.locality}\n"
                f"Описание: {self.description}\nТребования: {self.requirements}\nID Вакансии: {self.id_vac}\n"
                f"Более подробная информация по вакансии: {self.link}\n\n{"-" * 220}")

    def __repr__(self):
        """
        Метод для вывода отладочной информации об экземпляре класса
        """
        return (f"{self.__class__.__name__}({self.name}, {self.link}, {self.published_at}, {self.salary_min}, "
                f"{self.salary_max}, {self.currency}, {self.employer}, {self.locality}, {self.description}, "
                f"{self.requirements}, {self.id_vac})")

    def format_to_save_in_json(self):
        """
        Метод для форматирования экземпляра класса для дальнейшей записи в json файл
        """
        return {
            "name": self.name,
            "published_at": self.published_at,
            "salary min": self.salary_min,
            "salary max": self.salary_max,
            "currency": self.currency,
            "employer": self.employer,
            "locality": self.locality,
            "description": self.description,
            "requirements": self.requirements,
            "id": self.id_vac,
            "link": self.link,
        }


