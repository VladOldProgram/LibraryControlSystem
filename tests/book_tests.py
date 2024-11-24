import unittest
from unittest.mock import PropertyMock, patch
from Book import Book
import itertools


class TestBook(unittest.TestCase):
    def test_invalid_init(self):
        for i in range(3):
            attributes = ['non_empty'] * 3
            attributes[i] = ''
            self.assertRaises(
                Book.EmptyBookAttributeException, 
                Book, 
                title=attributes[0], 
                author=attributes[1], 
                year=attributes[2]
            )

    @patch.object(Book, '_Book__generate_id', new_callable=PropertyMock)
    def test_generating_id(self, generate_id_mock):
        generate_id_mock.return_value = itertools.count().__next__
        book_1 = Book('title', 'author', 'year')
        self.assertEqual(book_1.get_id(), 0)
        book_2 = Book('title', 'author', 'year')
        print(book_2.get_id())
        self.assertEqual(book_2.get_id(), 1)

    def test_set_valid_status(self):
        book = Book('title', 'author', 'year')
        status_code = len(Book.STATUSES) - 1
        book.set_status(status_code)
        self.assertEqual(book.get_status(), Book.STATUSES[status_code])

    def test_set_invalid_status(self):
        book = Book('title', 'author', 'year')
        status_code = len(Book.STATUSES)
        self.assertRaises(
            Book.IncorrectBookStatusException, 
            book.set_status, 
            status_code
        )


if __name__ == '__main__':
    unittest.main()
