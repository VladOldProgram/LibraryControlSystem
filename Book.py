from collections.abc import Callable
import itertools


class Book():
    """
    Класс книги.
    
    Attributes:
        __id (int): Целочисленный уникальный идентификатор, генерируется 
        автоматически
        title (str): Название
        author (str): Автор
        year (str): Год издания
        __status (str): Статус
        STATUSES (dict[int, str]): Возможные значения статуса 
        ("в наличии", "выдана")

    Classes:
        EmptyBookAttributeException: Ошибка пустого атрибута книги
        IncorrectBookStatusException: Ошибка некорректного статуса книги
        
    Methods:
        __generate_id (Callable[[], int]): Генерирует следующий целочисленный 
        идентификатор
        get_id (Callable[[], int]): Возвращает id книги
        get_status (Callable[[], str]): Возвращает статус книги
        set_book_status (Callable[[int], None]): Устанавливает статус книги
    """

    __id: int 
    __generate_id: Callable[[], int] = itertools.count().__next__
    title: str
    author: str
    year: str
    __status: str

    STATUSES: dict[int, str] = {0: 'в наличии', 1: 'выдана'}

    class EmptyBookAttributeException(Exception):
        """Ошибка пустого атрибута книги."""

        message = 'Ошибка: атрибуты книги не могут быть пустыми.'

        def __str__(self):
            return self.message

    class IncorrectBookStatusException(Exception):
        """Ошибка некорректного статуса книги."""

        message = 'Ошибка: указан некорректный статус книги.'

        def __str__(self):
            return self.message

    def __init__(self, title: str, author: str, year: str):
        """
        Инициализирует атрибуты __id, title, author, year, __status.
        
        Args: 
            title: Название
            author: Автор
            year: Год издания

        Raises:
            EmptyBookAttributeException
        """
        for attribute in [title, author, year]:
            if len(attribute) == 0:
                raise self.EmptyBookAttributeException
        self.__id = Book.__generate_id()
        self.title = title
        self.author = author
        self.year = year
        self.__status = self.STATUSES[0]

    def get_id(self) -> int:
        """Возвращает id книги."""
        return self.__id

    def get_status(self) -> str:
        """Возвращает статус книги."""
        return self.__status

    def set_status(self, status_code: int) -> None:
        """
        Устанавливает статус книги по его номеру.

        Args:
            status_code: номер статуса из STATUSES
            
        Raises:
            IncorrectBookStatusException

        Returns:
            None
        """
        if status_code >= len(self.STATUSES):
            raise self.IncorrectBookStatusException
        self.__status = self.STATUSES[status_code]





