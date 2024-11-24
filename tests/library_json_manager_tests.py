import unittest
from ConsoleLibrary import ConsoleLibrary
from JSONManager import LibraryJSONManager
from copy import deepcopy


class TestLibraryJSONManager(unittest.TestCase):
    def test_read_from_json(self):
        console_library = ConsoleLibrary()
        default_file_path = r'.\library.json'
        library_json_manager = LibraryJSONManager(
            default_file_path, 
            console_library
        )
        for i in range(3):
            console_library.add_book(f'book {i}', f'author {i}', f'year {i}')
        books_before_save = deepcopy(console_library.books)
        library_json_manager.save_to_json()
        for i in range(3):
            console_library.delete_book(i)
        library_json_manager.read_from_json()
        for actual_book, expected_book in zip(
            console_library.books.values(), 
            books_before_save.values()
        ):
            self.assertEqual(actual_book.title, expected_book.title)
            self.assertEqual(actual_book.author, expected_book.author)
            self.assertEqual(actual_book.year, expected_book.year)
            self.assertEqual(actual_book.get_status(), expected_book.get_status())


        


if __name__ == '__main__':
    unittest.main()
