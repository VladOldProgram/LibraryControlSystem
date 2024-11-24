from pathlib import Path
import json
from ConsoleLibrary import ConsoleLibrary
from Book import Book


class JSONManager():
    """
    Класс файлового менеджера.
    
    Attributes:
        __file_path (str): Путь до json-файла сохранения-загрузки.
        obj (object): Объект для сохранения-загрузки.
        
    Methods:
        get_file_path (Callable[[], None]): Возвращает путь до json-файла 
        сохранения-загрузки
        set_file_path (Callable[[str], None]): Устанавливает путь до json-файла 
        сохранения-загрузки
        save_to_json (Callable[[object], None]): Сохраняет объект в json-файл
        read_from_json (Callable[[object], None]): Загружает объект из json-файла
    """

    __file_path: str
    obj: object

    def __init__(self, file_path: str, obj: object):
        """
        Инициализирует атрибуты __file_path, obj.
        
        Args: 
            file_path: Путь до json-файла сохранения-загрузки
            obj: Объект для сохранения-загрузки

        Raises:
            FileNotFoundError: Ошибка несуществующего файла по указанному пути
        """
        if not Path(file_path).is_file():
            raise FileNotFoundError(
                f'Не существует файла по пути {file_path}'
            )
        self.__file_path = file_path
        self.obj = obj

    def get_file_path(self) -> str:
        """Возвращает путь до json-файла сохранения-загрузки."""
        return self.__file_path

    def set_file_path(self, file_path: str) -> None:
        """
        Устанавливает путь до json-файла сохранения-загрузки.
        
        Args: 
            file_path: Путь до json-файла сохранения-загрузки

        Raises:
            FileNotFoundError: Ошибка несуществующего файла по указанному пути

        Returns:
            None
        """
        if not Path(file_path).is_file():
            raise FileNotFoundError(
                f'Не существует файла по пути {file_path}'
            )
        self.__file_path = file_path

    def save_to_json(self) -> None:
        """Сохраняет объект в json-файл."""
        pass

    def read_from_json(self) -> None:
        """Загружает объект из json-файла."""
        pass


class LibraryJSONManager(JSONManager):
    """
    Класс файлового менеджера библиотеки.
    
    Attributes:
        obj (ConsoleLibrary): Библиотека для сохранения-загрузки.
        
    Methods:
        get_file_path (Callable[[], None]): Возвращает путь до json-файла 
        сохранения-загрузки
        set_file_path (Callable[[str], None]): Устанавливает путь до json-файла
        сохранения-загрузки
        save_to_json (Callable[[object], None]): Сохраняет библиотеку в 
        json-файл
        read_from_json (Callable[[object], None]): Загружает библиотеку из 
        json-файла
    """

    obj: ConsoleLibrary

    def save_to_json(self) -> None:
        """Сохраняет библиотеку в json-файл."""
        with open(self.get_file_path(), 'w') as f:
            json.dump(self.obj, f, default=lambda o: o.__dict__)

    def read_from_json(self) -> None:
        """Загружает библиотеку из json-файла."""
        with open(self.get_file_path(), 'r') as f:
            json_books = json.load(f)['books']
            self.obj.books.clear()
            for json_book in json_books.values():
                json_book.pop('_Book__id')
                json_book_status = json_book.pop('_Book__status')
                book = Book(**json_book)
                for i, status in book.STATUSES.items():
                    if json_book_status == status:
                        book.set_status(i)
                        break
                self.obj.books[book.get_id()] = book



