import unittest
from unittest.mock import PropertyMock, patch
from Book import Book
import itertools
from ConsoleLibrary import ConsoleLibrary
import io
import sys


class TestConsoleLibrary(unittest.TestCase):
    @patch.object(Book, '_Book__generate_id', new_callable=PropertyMock)
    def test_print_book_by_valid_id(self, generate_id_mock):
        generate_id_mock.return_value = itertools.count().__next__
        book = Book('title', 'author', 'year')
        console_library = ConsoleLibrary({book.get_id(): book})
        captured_output = io.StringIO() 
        sys.stdout = captured_output
        id = 0
        console_library.print_book(id)  
        sys.stdout = sys.__stdout__  
        expected_print = ConsoleLibrary.BOOK_PRINT_PATTERN.format(
            id, 
            'title', 
            'author', 
            'year',
            Book.STATUSES[0]
        ) + '\n'
        self.assertEqual(captured_output.getvalue(), expected_print)

    @patch.object(Book, '_Book__generate_id', new_callable=PropertyMock)
    def test_print_book_by_invalid_id(self, generate_id_mock):
        generate_id_mock.return_value = itertools.count().__next__
        book = Book('title', 'author', 'year')
        console_library = ConsoleLibrary({book.get_id(): book})
        captured_output = io.StringIO() 
        sys.stdout = captured_output
        id = 1
        console_library.print_book(id)  
        sys.stdout = sys.__stdout__  
        expected_print = 'Книга не найдена.\n'
        self.assertEqual(captured_output.getvalue(), expected_print)

    @patch.object(Book, '_Book__generate_id', new_callable=PropertyMock)
    def test_valid_print_books(self, generate_id_mock):
        generate_id_mock.return_value = itertools.count().__next__
        book_1 = Book('title', 'author', 'year')
        book_2 = Book('title', 'author', 'year')
        console_library = ConsoleLibrary({
            book_1.get_id(): book_1, 
            book_2.get_id(): book_2
        })
        captured_output = io.StringIO() 
        sys.stdout = captured_output
        console_library.print_books()  
        sys.stdout = sys.__stdout__  
        expected_print = ConsoleLibrary.BOOK_PRINT_PATTERN.format(
            0, 
            'title', 
            'author', 
            'year',
            Book.STATUSES[0]
        ) + '\n' + ConsoleLibrary.BOOK_PRINT_PATTERN.format(
            1, 
            'title', 
            'author', 
            'year',
            Book.STATUSES[0]
        ) + '\n'
        self.assertEqual(captured_output.getvalue(), expected_print)

    def test_print_books_in_empty_library(self):
        console_library = ConsoleLibrary()
        captured_output = io.StringIO() 
        sys.stdout = captured_output
        console_library.print_books()  
        sys.stdout = sys.__stdout__  
        expected_print = 'Библиотека пуста.\n'
        self.assertEqual(captured_output.getvalue(), expected_print)

    @patch.object(Book, '_Book__generate_id', new_callable=PropertyMock)
    def test_find_book_by_valid_key_word(self, generate_id_mock):
        generate_id_mock.return_value = itertools.count().__next__
        book = Book('Война и мир', 'Толстой Л. Н.', '1869')
        console_library = ConsoleLibrary({book.get_id(): book})
        captured_output = io.StringIO() 
        sys.stdout = captured_output
        key_word = 'Толстой'
        console_library.find_book(key_word)  
        sys.stdout = sys.__stdout__  
        expected_print = ConsoleLibrary.BOOK_PRINT_PATTERN.format(
            0, 
            'Война и мир', 
            'Толстой Л. Н.', 
            '1869',
            Book.STATUSES[0]
        ) + '\n'
        self.assertEqual(captured_output.getvalue(), expected_print)

    def test_find_book_by_invalid_key_word(self):
        book = Book('Война и мир', 'Толстой Л. Н.', '1869')
        console_library = ConsoleLibrary({book.get_id(): book})
        captured_output = io.StringIO() 
        sys.stdout = captured_output
        key_word = 'Толстой.'
        console_library.find_book(key_word)  
        sys.stdout = sys.__stdout__  
        expected_print = 'Книга не найдена.\n'
        self.assertEqual(captured_output.getvalue(), expected_print)

    def test_add_valid_book(self):
        console_library = ConsoleLibrary()
        captured_output = io.StringIO() 
        sys.stdout = captured_output
        console_library.add_book('title', 'author', 'year')
        self.assertEqual(len(console_library.books), 1)
        self.assertEqual(console_library.books[0].title, 'title')
        self.assertEqual(console_library.books[0].author, 'author')
        self.assertEqual(console_library.books[0].year, 'year')
        sys.stdout = sys.__stdout__  
        expected_print = 'Книга добавлена.\n'
        self.assertEqual(captured_output.getvalue(), expected_print)

    def test_add_invalid_book(self):
        console_library = ConsoleLibrary()
        captured_output = io.StringIO() 
        sys.stdout = captured_output
        console_library.add_book('', 'author', 'year')
        sys.stdout = sys.__stdout__  
        expected_print = Book.EmptyBookAttributeException.message + '\n'
        self.assertEqual(captured_output.getvalue(), expected_print)
        self.assertEqual(len(console_library.books), 0)

    def test_change_valid_book_status(self):
        book = Book('title', 'author', 'year')
        console_library = ConsoleLibrary({book.get_id(): book})
        captured_output = io.StringIO() 
        sys.stdout = captured_output
        status_code = len(Book.STATUSES) - 1
        console_library.change_book_status(book.get_id(), status_code)  
        sys.stdout = sys.__stdout__  
        expected_print = 'Статус книги изменен.\n'
        self.assertEqual(captured_output.getvalue(), expected_print)
        self.assertEqual(book.get_status(), Book.STATUSES[status_code])

    def test_change_invalid_book_status(self):
        book = Book('title', 'author', 'year')
        console_library = ConsoleLibrary({book.get_id(): book})
        captured_output = io.StringIO() 
        sys.stdout = captured_output
        status_code = len(Book.STATUSES)
        console_library.change_book_status(book.get_id(), status_code)  
        sys.stdout = sys.__stdout__  
        expected_print = Book.IncorrectBookStatusException.message + '\n'
        self.assertEqual(captured_output.getvalue(), expected_print)

    @patch.object(Book, '_Book__generate_id', new_callable=PropertyMock)
    def test_change_book_status_by_invalid_id(self, generate_id_mock):
        generate_id_mock.return_value = itertools.count().__next__
        book = Book('title', 'author', 'year')
        console_library = ConsoleLibrary({book.get_id(): book})
        captured_output = io.StringIO() 
        sys.stdout = captured_output
        status_code = len(Book.STATUSES) - 1
        id = 1
        console_library.change_book_status(id, status_code)  
        sys.stdout = sys.__stdout__  
        expected_print = 'Книга не найдена.\n'
        self.assertEqual(captured_output.getvalue(), expected_print)

    @patch.object(Book, '_Book__generate_id', new_callable=PropertyMock)
    def test_delete_book_by_valid_id(self, generate_id_mock):
        generate_id_mock.return_value = itertools.count().__next__
        book = Book('title', 'author', 'year')
        console_library = ConsoleLibrary({book.get_id(): book})
        captured_output = io.StringIO() 
        sys.stdout = captured_output
        id = 0
        console_library.delete_book(id)  
        sys.stdout = sys.__stdout__  
        expected_print = 'Книга удалена.\n'
        self.assertEqual(captured_output.getvalue(), expected_print)
        self.assertEqual(len(console_library.books), 0)

    @patch.object(Book, '_Book__generate_id', new_callable=PropertyMock)
    def test_delete_book_by_invalid_id(self, generate_id_mock):
        generate_id_mock.return_value = itertools.count().__next__
        book = Book('title', 'author', 'year')
        console_library = ConsoleLibrary({book.get_id(): book})
        captured_output = io.StringIO() 
        sys.stdout = captured_output
        id = 1
        console_library.delete_book(id)  
        sys.stdout = sys.__stdout__  
        expected_print = 'Книга не найдена.\n'
        self.assertEqual(captured_output.getvalue(), expected_print)
        self.assertEqual(len(console_library.books), 1)


if __name__ == '__main__':
    unittest.main()
