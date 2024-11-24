from Book import Book


class ConsoleLibrary():
    """
    Класс консольной библиотеки.
    
    Attributes:
        books (dict[int, Book]): Книги в библиотеке
        BOOK_PRINT_PATTERN (str): Шаблон для печати полей книг
        
    Methods:
        print_book (Callable[[int], None]): Печатает поля книги из библиотеки
        print_books (Callable[[], None]): Печатает поля всех книг в библиотеке
        find_book (Callable[[str], None]): Ищет книгу в библиотеке и печатает 
        ее поля
        add_book (Callable[[str, str, str], None]): Добавляет книгу в библиотеку
        change_book_status (Callable[[int, int], None]): Меняет статус книги в 
        библиотеке
        delete_book (Callable[[int], None]): Удаляет книгу из библиотеки
    """

    books: dict[int, Book]

    BOOK_PRINT_PATTERN: str = '\t- id={0} \"{1}\", {2}, {3} г. - {4}.'

    def __init__(self, books: dict[int, Book] = None):
        """
        Инициализирует атрибут books.
        
        Args: 
            books: Книги для начального наполнения библиотеки
        """
        if books is not None:
            self.books = books
        else:
            self.books = {}

    def print_book(self, id: int) -> None:
        """
        Печатает поля книги по ее id. В случае неудачи поиска печатает 
        "Книга не найдена.".

        Args:
            id: id книги

        Returns:
            None
        """
        if id not in self.books.keys():
            print('Книга не найдена.')
            return
        book = self.books[id]
        print(self.BOOK_PRINT_PATTERN.format(
            book.get_id(), 
            book.title, 
            book.author, 
            book.year, 
            book.get_status()
        ))

    def print_books(self) -> None:
        """
        Печатает поля всех книг в библиотеке. В случае отсутствия книг в 
        библиотеке печатает "Библиотека пуста.".

        Returns:
            None
        """
        if len(self.books) == 0:
            print('Библиотека пуста.')
            return
        for book in self.books.values():
            print(self.BOOK_PRINT_PATTERN.format(
                book.get_id(), 
                book.title, 
                book.author, 
                book.year, 
                book.get_status()
            ))

    def find_book(self, key_word: str) -> None:
        """
        Ищет книгу в библиотеке по названию, автору или году издания и печатает
        ее поля. В случае неудачи поиска печатает "Книга не найдена.".

        Args:
            key_word: ключевое слово для поиска

        Returns:
            None
        """
        book_is_found = False
        for book in self.books.values():
            attribute_values_for_searching = [
                book.title, 
                book.author, 
                book.year
            ]
            for attribute_value in attribute_values_for_searching:
                if key_word in attribute_value:
                    self.print_book(book.get_id())
                    book_is_found = True
                    break
        if not book_is_found:
            print('Книга не найдена.')

    def add_book(self, title: str, author: str, year: str) -> None:
        """
        Добавляет книгу в библиотеку. В случае успешного добавления печатает 
        "Книга добавлена.". В случае возникновения исключения печатает его 
        описание.

        Args:
            title: Название книги
            author: Автор книги
            year: Год издания книги

        Returns:
            None
        """
        try:
            book = Book(title, author, year)
        except Book.EmptyBookAttributeException as e:
            print(e)
            return
        self.books[book.get_id()] = book
        print('Книга добавлена.')

    def change_book_status(self, id: int, status_code: int) -> None:
        """
        Меняет статус книги в библиотеке. В случае успешного изменения печатает
        "Статус книги изменен.". В случае неудачи поиска печатает 
        "Книга не найдена.". В случае возникновения исключения печатает его 
        описание.

        Args:
            id: id книги
            status_code: номер статуса из Book.STATUSES

        Returns:
            None
        """
        if id not in self.books.keys():
            print('Книга не найдена.')
            return
        try:
            self.books[id].set_status(status_code)
        except Book.IncorrectBookStatusException as e:
            print(e)
            return
        print('Статус книги изменен.')

    def delete_book(self, id: int) -> None:
        """
        Удаляет книгу из библиотеки. В случае успешного удаления печатает
        "Книга удалена.". В случае неудачи поиска печатает "Книга не найдена.".

        Args:
            id: id книги

        Returns:
            None
        """
        if id not in self.books.keys():
            print('Книга не найдена.')
            return
        self.books.pop(id)
        print('Книга удалена.')




