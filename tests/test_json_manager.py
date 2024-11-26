import unittest
import os
from utils.data import JsonManager
from models.book import Book


class TestJsonManager(unittest.TestCase):
    def setUp(self):
        self.manager = JsonManager()
        self.test_file = "test_library.json"
        self.temp_file = "test_library.tmp"

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)

    def test_save_and_load_data(self):
        books = [Book(id=1, title="Тестовая книга", author="Автор", year=2020)]

        self.manager.save_data(
            books, data_file=self.test_file, temp_file=self.temp_file
        )

        loaded_books = self.manager.load_data(data_file=self.test_file)

        self.assertEqual(len(loaded_books), 1)
        self.assertEqual(loaded_books[0].title, "Тестовая книга")
        self.assertEqual(loaded_books[0].author, "Автор")

    def test_load_empty_file(self):
        with open(self.test_file, "w") as f:
            f.write("")
        books = self.manager.load_data(data_file=self.test_file)
        self.assertEqual(len(books), 0)

    def test_load_invalid_json(self):
        with open(self.test_file, "w") as f:
            f.write("{invalid_json}")
        books = self.manager.load_data(data_file=self.test_file)
        self.assertEqual(len(books), 0)


if __name__ == "__main__":
    unittest.main()
