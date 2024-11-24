from argparse import ArgumentTypeError
from collections.abc import Callable
from types import NoneType
from typing import Any
from Singleton import Singleton
from inspect import signature
import itertools


class Console(metaclass=Singleton):
    """
    Класс консоли, реализует паттерн Singleton.
    
    Attributes:
        __commands (dict[str, tuple[Callable[[Any], Any], str]]): 
        Зарегистрированные команды
        
    Methods:
        register_command (Callable[[str, Callable[[Any], Any], str], None]): 
        Регистрирует команду
        print_commands (Callable[[], None]): Печатает все зарегистрированные
        команды
        parse_command (Callable[[str], tuple[str, list[str]]]): Разбирает ввод 
        с консоли на команду и аргументы
        cast (Callable[[str, Any], Any]): Приводит аргумент к int, str или
        float
        start (Callable[[], None]): Запускает бесконечный цикл ввода-вывода 
        консоли
    """

    __commands: dict[str, tuple[Callable[[Any], Any], str]]

    def __init__(
        self, 
        commands: dict[str, tuple[Callable[[Any], Any], str]] = None
    ):
        """
        Инициализирует атрибут __commands. Регистрирует команду "help" для 
        печати списка всех доступных команд.
        
        Args: 
            commands: Команды для начальной регистрации
        """
        if commands is not None:
            self.__commands = commands
        else:
            self.__commands = {}
        self.register_command(
            'help', 
            self.print_commands, 
            'Выводит список всех доступных команд.'
        )

    def register_command(
        self, 
        name: str, 
        func: Callable[[Any], Any], 
        description: str
    ) -> None:
        """
        Регистрирует команду. При регистрации команды с одинаковым названием
        перезапишет старую команду.

        Args:
            name: Название команды
            func: Функция для вызова по этой команде
            description: Описание команды для вывода в help

        Raises:
            ValueError: Название команды не может быть пустой строкой

        Returns:
            None
        """
        if len(name) == 0:
            raise ValueError('Command name cannot be empty string.')
        self.__commands[name] = (func, description)

    def print_commands(self) -> None:
        """Печатает все зарегистрированные команды."""
        print('Вы можете использовать следующие команды:')
        for command in self.__commands:
            print(f'\t- {command}: {self.__commands[command][1]}')

    def parse_command(self, command: str) -> tuple[str, list[str]]:
        """
        Разбирает ввод с консоли на команду и аргументы.

        Args:
            command: Строка-команда с аргументами

        Returns:
            Кортеж из команды и списка аргументов
        """
        parsed_command = command.split()
        if len(parsed_command) == 0:
            return ('', [])
        return parsed_command[0], parsed_command[1:]

    def cast(self, type_to_cast: str, arg: Any) -> Any:
        """
        Приводит аргумент к int, str или float.

        Args:
            type_to_cast: Тип данных int, str или float в строчном 
            представлении
            arg: Аргумент для приведения

        Returns:
            Неприведенный аргумент при отсутствии type_to_cast или аргумент, 
            приведенный к int/str/float, или None иначе
        """
        if type_to_cast is None:
            return arg
        elif type_to_cast == 'int':
            return int(arg)
        elif type_to_cast == 'str':
            return str(arg)
        elif type_to_cast == 'float':
            return float(arg)

    def start(self) -> None:
        """
        Запускает бесконечный цикл ввода-вывода консоли:
            1) ожидает ввода пользователя;
            2) разбирает ввод на команду и аргументы (печатает 
            "Ошибка: неизвестная команда." в случае незарегистрированной 
            команды);
            3) получает сигнатуру соответствующей команде функции (печатает
            "Ошибка: {command} принимает {len(func_args)} аргументов, но 
            передано {len(given_args)}." в случае несовпадения числа требуемых
            и переданных аргументов);
            4) приводит переданные аргументы к соответствующим типам требуемых 
            аргументов (печатает "Ошибка: не удалось привести тип аргумента." в 
            случае неудачи приведения типа);
            5) вызывает соответствующую команде функцию с приведенными 
            переданными аргументами.
        В случае возникновения исключения на шагах 4, 5 печатает его описание.
        """
        for _ in itertools.count():
            # 1, 2)
            command, given_args = self.parse_command(input())
            if command not in self.__commands:
                print('Ошибка: неизвестная команда.')
                continue
            func = self.__commands[command][0]
            # 3)
            func_args = signature(func).parameters
            if len(given_args) != len(func_args):
                print(f'Ошибка: {command} принимает'
                      f' {len(func_args)} аргументов,'
                      f' но передано {len(given_args)}.')
                continue
            try:
                # 4)
                parsed_args = []
                for given_arg, func_arg_key in zip(given_args, func_args.keys()):
                    splited_parameter = str(func_args[func_arg_key]).split(': ')
                    if len(splited_parameter) == 1:
                        func_arg_type = None
                    else:
                        func_arg_type = splited_parameter[1]
                    casted_given_arg = self.cast(func_arg_type, given_arg)
                    if casted_given_arg is None:
                        raise ArgumentTypeError(
                            'Ошибка: не удалось привести тип аргумента.'
                        )
                    parsed_args.append(casted_given_arg)
                # 5)
                func(*parsed_args)
            except Exception as e:
                print(e)





