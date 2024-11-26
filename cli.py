from abc import ABC, abstractmethod
from services.library import LibraryServiceInterface
from models.status import BookStatus
from models.book import Book


class BaseUI(ABC):
    """Базовый абстрактный класс интерфейса пользователя."""

    @abstractmethod
    def run(self):
        """Запуск основного цикла программы."""
        pass


class ConsoleUI(BaseUI):
    """Консольная реализация интерфейса пользователя."""

    def __init__(self, library_service: LibraryServiceInterface):
        self.library_service = library_service

    def run(self):
        """Запуск основного цикла программы."""

        actions = {
            "1": self.add_book,
            "2": self.remove_book,
            "3": self.search_books,
            "4": self.display_books,
            "5": self.change_book_status,
            "6": self.exit_program,
        }

        while True:
            print("\n===== Система управления библиотекой =====")
            print("1. Добавить книгу")
            print("2. Удалить книгу")
            print("3. Поиск книги")
            print("4. Отобразить все книги")
            print("5. Изменить статус книги")
            print("6. Выход")
            choice = input("Выберите действие (1-6): ").strip()

            action = actions.get(choice)

            if action:
                action()
            else:
                print("Некорректное действие, попробуйте снова.")

    def add_book(self):
        """Добавляет новую книгу в библиотеку."""
        title = input("Введите название книги: ").strip()
        author = input("Введите автора книги: ").strip()
        year_input = input("Введите год издания книги: ").strip()

        if not title or not author or not year_input:
            print("Все поля должны быть заполнены.")
            return

        try:
            year = int(year_input)
        except ValueError:
            print("Год издания должен быть числом.")
            return

        new_book = self.library_service.add_book(title, author, year)

        print(f"Книга '{new_book.title}' успешно добавлена с ID {new_book.id}.")

    def remove_book(self):
        """Удаляет книгу по ID."""
        id_input = input("Введите ID книги для удаления: ").strip()

        try:
            book_id = int(id_input)
        except ValueError:
            print("ID должен быть числом.")
            return

        removed = self.library_service.remove_book(book_id)

        if removed:
            print(f"Книга с ID {book_id} успешно удалена.")
        else:
            print(f"Книга с ID {book_id} не найдена.")

    def search_books(self):
        """Ищет книги по заданному критерию."""
        criteria = {"1": "название", "2": "автор", "3": "год"}

        print("Выберите критерий поиска:")
        print("1. Название")
        print("2. Автор")
        print("3. Год издания")

        choice = input("Введите номер критерия: ").strip()

        criterion = criteria.get(choice)

        if not criterion:
            print("Некорректный выбор.")
            return

        keyword = input(f"Введите {criterion}: ").strip()
        result = self.library_service.search_books(keyword, criterion)

        if result:
            self.display_books(result)
        else:
            print("Книги по заданному критерию не найдены.")

    def display_books(self, books: list[Book] | None = None):
        """Отображает список книг."""
        books = books if books is not None else self.library_service.get_all_books()

        if not books:
            print("Список книг пуст.")
            return

        for book in books:
            print(
                f"ID: {book.id} | Название: {book.title} | Автор: {book.author} | Год: {book.year} | Статус: {book.status}"
            )

    def change_book_status(self):
        """Изменяет статус книги по ID."""
        id_input = input("Введите ID книги для изменения статуса: ").strip()

        try:
            book_id = int(id_input)
        except ValueError:
            print("Некорректный ID.")
            return

        book = self.library_service.find_book_by_id(book_id)

        if not book:
            print(f"Книга с ID {book_id} не найдена.")
            return

        print("Выберите статус:")
        print(f"1. {BookStatus.AVAILABLE.value}")
        print(f"2. {BookStatus.BORROWED.value}")

        choice = input("Введите номер статуса: ").strip()
        statuses = {"1": BookStatus.AVAILABLE.value, "2": BookStatus.BORROWED.value}
        status = statuses.get(choice)

        if not status:
            print("Некорректный выбор.")
            return

        success = self.library_service.change_book_status(book_id, status)

        if success:
            print(f"Статус книги с ID {book_id} изменен на '{status}'.")

        else:
            print("Ошибка при изменении статуса книги.")

    def exit_program(self):
        """Выходит из программы."""
        print("Выход из программы.")
        exit()
