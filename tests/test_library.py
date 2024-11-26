import unittest

from services.library import LibraryService
from models.status import BookStatus
from tests.mock_data_manager import MockDataManager


class TestLibraryService(unittest.TestCase):
    def setUp(self):
        self.mock_data_manager = MockDataManager()
        self.library_service = LibraryService(self.mock_data_manager)

    def test_add_book(self):
        book = self.library_service.add_book("Книга 1", "Автор 1", 2022)
        self.assertEqual(book.title, "Книга 1")
        self.assertEqual(len(self.library_service.get_all_books()), 1)

    def test_remove_book(self):
        self.library_service.add_book("Книга 1", "Автор 1", 2022)
        self.assertTrue(self.library_service.remove_book(1))
        self.assertEqual(len(self.library_service.get_all_books()), 0)

    def test_search_books(self):
        self.library_service.add_book("Книга 1", "Автор 1", 2022)
        self.library_service.add_book("Книга 2", "Автор 2", 2021)
        results = self.library_service.search_books("Книга", "название")
        self.assertEqual(len(results), 2)

    def test_change_book_status(self):
        self.library_service.add_book("Книга 1", "Автор 1", 2022)
        success = self.library_service.change_book_status(1, BookStatus.BORROWED.value)
        self.assertTrue(success)
        book = self.library_service.find_book_by_id(1)
        self.assertEqual(book.status, BookStatus.BORROWED.value)

    def test_remove_nonexistent_book(self):
        self.assertFalse(self.library_service.remove_book(99))

    def test_search_books_no_result(self):
        results = self.library_service.search_books("Несуществующая", "название")
        self.assertEqual(len(results), 0)

    def test_change_book_status_invalid_id(self):
        success = self.library_service.change_book_status(99, BookStatus.BORROWED.value)
        self.assertFalse(success)

    def test_find_book_by_id_invalid(self):
        book = self.library_service.find_book_by_id(99)
        self.assertIsNone(book)


if __name__ == "__main__":
    unittest.main()
