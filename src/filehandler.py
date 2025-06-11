import json
import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List


class FileHandler(ABC):
    def __init__(self, filename: str) -> None:
        """
        Инициализирует экземпляр FileHandler с указанным именем файла.

        :param filename: Имя файла, с которым будет работать обработчик.
        """
        self.__filename = filename

    @abstractmethod
    def add_vacancy(self, vacancy: Dict[str, Any]) -> None:
        """
        Добавляет вакансию в файл.

        :param vacancy: Словарь с данными вакансии.
        """
        pass

    @abstractmethod
    def get_vacancies(self, **criteria: Any) -> List[Dict[str, Any]]:
        """
        Получает список вакансий на основе заданных критериев.

        :param criteria: Критерии для фильтрации вакансий.
        :return: Список вакансий, соответствующих критериям.
        """
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy_id: str) -> None:
        """
        Удаляет вакансию по указанному идентификатору.

        :param vacancy_id: Идентификатор вакансии для удаления.
        """
        pass


class JSONFileHandler(FileHandler):
    def __init__(self, filename: str = "Data/vacancies.json") -> None:
        """
        Инициализирует экземпляр JSONFileHandler с указанным именем файла.

        :param filename: Имя файла JSON, с которым будет работать обработчик.
        """
        super().__init__(filename)

    def add_vacancy(self, vacancy: Dict[str, Any]) -> None:
        """Метод для добавления вакансии в файл."""
        vacancies = self.get_vacancies()
        if vacancy not in vacancies:
            vacancies.append(vacancy)
            with open(self._FileHandler__filename, "w") as f:
                json.dump(vacancies, f, indent=4)

    def get_vacancies(self, **criteria: Any) -> List[Dict[str, Any]]:
        """Метод для получения вакансий по указанным критериям."""
        if not os.path.exists(self._FileHandler__filename):
            return []

        with open(self._FileHandler__filename, "r") as f:
            vacancies = json.load(f)

        if criteria:
            filtered_vacancies = []
            for vacancy in vacancies:
                if all(vacancy.get(key) == value for key, value in criteria.items()):
                    filtered_vacancies.append(vacancy)
            return filtered_vacancies

        return vacancies

    def delete_vacancy(self, vacancy_id: str) -> None:
        """Метод для удаления вакансии по идентификатору."""
        vacancies = self.get_vacancies()
        vacancies = [
            vacancy for vacancy in vacancies if vacancy.get("id") != vacancy_id
        ]

        with open(self._FileHandler__filename, "w") as f:
            json.dump(vacancies, f, indent=4)
