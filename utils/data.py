from abc import ABC, abstractmethod
from dataclasses import asdict
import json
import os

from models.book import Book


class DataManagerInterface(ABC):
    """Абстрактный базовый класс для управления данными библиотеки."""

    @abstractmethod
    def load_data(self) -> list[Book]:
        """Загружает данные из хранилища."""
        pass

    @abstractmethod
    def save_data(self, books: list[Book]) -> None:
        """Сохраняет данные в хранилище."""
        pass


class JsonManager(DataManagerInterface):
    """Класс для управления данными библиотеки в формате JSON."""

    DATA_FILE = "library.json"
    TEMP_FILE = "library.tmp"

    def load_data(self, data_file: str = DATA_FILE) -> list[Book]:
        """Загружает данные из файла JSON."""
        try:
            with open(data_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                return [Book(**item) for item in data]

        except FileNotFoundError:
            return []

        except json.JSONDecodeError as e:
            print(f"Ошибка чтения данных из файла {data_file}: {e}")
            return []

    def save_data(
        self,
        books: list[Book],
        data_file: str = DATA_FILE,
        temp_file: str = TEMP_FILE,
    ) -> None:
        """Сохраняет данные в файл JSON."""
        try:
            with open(data_file, "w", encoding="utf-8") as file:
                data = [asdict(item) for item in books]
                json.dump(data, file, ensure_ascii=False, indent=2)

            os.replace(temp_file, data_file)

        except (IOError, json.JSONDecodeError) as e:
            print(f"Ошибка записи данных в файл {data_file}: {e}")

            if os.path.exists(temp_file):
                os.remove(temp_file)
