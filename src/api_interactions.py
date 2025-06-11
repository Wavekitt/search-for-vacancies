import abc
from typing import List, Dict, Any, Optional
import requests


class JobAPI(abc.ABC):
    @abc.abstractmethod
    def _connect(self) -> requests.Response:
        """Метод для подключения к API"""
        pass

    @abc.abstractmethod
    def get_vacancies(self, keyword: str, cantidad: int) -> List[Dict[str, Any]]:
        """Метод для получения вакансий по ключевому слову"""
        pass


class hh_API(JobAPI):
    BASE_URL = "https://api.hh.ru/vacancies"

    def __init__(self) -> None:
        self.__session: Optional[requests.Session] = None

    def _connect(self) -> requests.Response:
        """Метод для подключения к API"""
        self.__session = requests.Session()
        response = self.__session.get(self.BASE_URL)
        response.raise_for_status()
        return response

    def get_vacancies(self, keyword: str, cantidad: int) -> List[Dict[str, Any]]:
        """Метод для получения вакансий по ключевому слову"""
        self._connect()

        params = {"text": keyword, "per_page": cantidad}

        response = self.__session.get(self.BASE_URL, params=params)
        response.raise_for_status()

        vacancies = response.json().get("items", [])
        return [
            {
                "name": vacancy["name"],
                "company": vacancy["employer"]["name"],
                "url": vacancy["alternate_url"],
                "salary": vacancy.get("salary"),
                "id": vacancy.get("id"),
            }
            for vacancy in vacancies
        ]


if __name__ == "__main__":
    hh_api = hh_API()
    try:
        vacancies = hh_api.get_vacancies("Python", 10)
        for vacancy in vacancies:
            salary = vacancy["salary"]
            if salary and salary["from"] is not None and salary["to"] is not None:
                average_salary = salary["from"] + (salary["to"] - salary["from"]) / 2
            elif salary and salary["from"] is not None:
                average_salary = salary["from"]
            elif salary and salary["to"] is not None:
                average_salary = salary["to"]
            else:
                average_salary = 0

            print(
                f"Название вакансии: {vacancy['name']}, Работодатель: {vacancy['company']}, "
                f"Ссылка: {vacancy['url']}, Средняя зарплата: {average_salary}, id: {vacancy['id']}"
            )
    except Exception as e:
        print(f"Произошла ошибка: {e}")
