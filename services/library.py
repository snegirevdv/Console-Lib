from abc import ABC, abstractmethod

from models.book import Book
from models.status import BookStatus
from utils.data import DataManagerInterface


class LibraryServiceInterface(ABC):
    """Интерфейс для сервиса библиотеки."""

    @abstractmethod
    def add_book(self, title: str, author: str, year: int) -> Book:
        """Добавляет новую книгу в библиотеку."""
        pass

    @abstractmethod
    def remove_book(self, book_id: int) -> bool:
        """Удаляет книгу по ID."""
        pass

    @abstractmethod
    def search_books(self, keyword: str, criterion: str) -> list[Book]:
        """Находит книги по ключевому слову и критерию."""
        pass

    @abstractmethod
    def get_all_books(self) -> list[Book]:
        """Получает список всех книг."""
        pass

    @abstractmethod
    def change_book_status(self, book_id: int, status: BookStatus) -> bool:
        """Изменяет статус книги."""
        pass

    @abstractmethod
    def find_book_by_id(self, book_id: int) -> Book | None:
        """Находит книгу по ID."""
        pass


class LibraryService(LibraryServiceInterface):
    """Сервис для управления библиотекой."""

    def __init__(self, data_manager: DataManagerInterface):
        self._data_manager = data_manager
        self._books: list[Book] = self._data_manager.load_data()

    def _get_next_id(self) -> int:
        return max(book.id for book in self._books) + 1 if self._books else 1

    def get_all_books(self) -> list[Book]:
        """Получает список всех книг."""
        return self._books

    def search_books(self, keyword: str, criterion: str) -> list[Book]:
        """Находит книги по ключевому слову и критерию."""
        keyword = keyword.lower()

        match criterion:
            case "название":
                return [book for book in self._books if keyword in book.title.lower()]
            case "автор":
                return [book for book in self._books if keyword in book.author.lower()]
            case "год":
                try:
                    return [book for book in self._books if book.year == int(keyword)]
                except ValueError:
                    return []

        return []

    def add_book(self, title: str, author: str, year: int) -> Book:
        """Добавляет новую книгу в библиотеку."""
        new_book = Book(id=self._get_next_id(), title=title, author=author, year=year)
        self._books.append(new_book)
        self._data_manager.save_data(self._books)
        return new_book

    def remove_book(self, book_id: int) -> bool:
        """Удаляет книгу по ID."""
        book = self.find_book_by_id(book_id)

        if book:
            self._books.remove(book)
            self._data_manager.save_data(self._books)
            return True

        return False

    def change_book_status(self, book_id: int, status: str) -> bool:
        """Изменяет статус книги."""
        book = self.find_book_by_id(book_id)

        if book and status in BookStatus.get_available_statuses():
            book.status = status
            self._data_manager.save_data(self._books)
            return True

        return False

    def find_book_by_id(self, book_id: int) -> Book | None:
        """Находит книгу по ID."""
        return next((book for book in self._books if book.id == book_id), None)
