import requests
from abc import ABC, abstractmethod
from work_with_vacancies import WorkWithVacancies


class API(ABC):
    """
    Абстрактный класс для работы с API
    """

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_vacs(self, name, only_with_salary, area):
        pass


class HeadHunterAPI(API):
    """
    Класс для работы с API hh.ru
    """
    def __init__(self, api_url='https://api.hh.ru/vacancies'):
        """
        Конструктор класса
        """
        self.api_url = api_url

    def get_vacs(self, name, only_with_salary=False, area=None):
        """
        Метод для получения вакансий по заданным параметрам с сайта hh.ru.
        Возвращает экземпляр класса WorkWithVacancies.
        """

        params = {
            "text": name,
            "page": 0,
            "per_page": 100,
            "only_with_salary": only_with_salary,
            "area": area
        }
        response = requests.get(self.api_url, params)

        return [
            WorkWithVacancies(
                vac_info["name"],
                vac_info["employer"]["name"],
                vac_info["alternate_url"],
                vac_info["published_at"],
                (vac_info.get('salary', {}) or {}).get('from', 0),
                (vac_info.get('salary', {}) or {}).get('to', 0),
                (vac_info.get('salary', {}) or {}).get('currency', 0),
                vac_info["area"]["name"],
                vac_info["snippet"]["responsibility"],
                vac_info["id"],
                vac_info["snippet"]["requirement"]
            )
            for vac_info in response.json()["items"]
        ]
