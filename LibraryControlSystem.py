from Console import Console
from ConsoleLibrary import ConsoleLibrary
from JSONManager import LibraryJSONManager


def main() -> None:    
    # Создание консольной библиотеки
    console_library = ConsoleLibrary()
    # Создание Singleton-консоли
    console = Console()
    # Создание файлового менеджера
    default_file_path = r'.\library.json'
    library_json_manager = LibraryJSONManager(
        default_file_path, 
        console_library
    )
    # Регистрация команд управления библиотекой
    console.register_command(
        'add_book', 
        console_library.add_book,
        'Добавляет книгу в библиотеку. Принимает title, author, year.'
    )
    console.register_command(
        'delete_book', 
        console_library.delete_book,
        'Удаляет книгу из библиотеки. Принимает id.'
    )
    console.register_command(
        'find_book', 
        console_library.find_book,
        'Ищет книгу в библиотеке по названию, автору или году. ' \
        'Принимает key_word.'
    )
    console.register_command(
        'show_books', 
        console_library.print_books,
        'Отображает все книги библиотеки.'
    )
    console.register_command(
        'change_book_status', 
        console_library.change_book_status,
        'Меняет статус книги в библиотеке. ' \
        'Принимает id, status_code (0: в наличии, 1: выдана).'
    )
    # Регистрация команд сохранения-загрузки библиотеки
    console.register_command(
        'change_path', 
        library_json_manager.set_file_path,
        'Меняет путь до json-файла для сохранения-загрузки библиотеки.'
    )
    console.register_command(
        'save_library', 
        library_json_manager.save_to_json,
        'Сохраняет библиотеку в json-файл по установленному пути.'
    )
    console.register_command(
        'load_library', 
        library_json_manager.read_from_json,
        'Загружает библиотеку из json-файла по установленному пути.'
    )
    # Печать списка всех доступных команд системы управления библиотекой
    console.print_commands()
    # Старт работы системы управления библиотекой
    console.start()


if __name__ == '__main__':
    main()