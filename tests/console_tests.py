import unittest
from unittest.mock import patch
from Console import Console
import io
import sys


class TestConsole(unittest.TestCase):
    def setUp(self):
        console = Console()
        cmds = console._Console__commands
        [cmds.pop(k) for k in list(cmds.keys()) if k != 'help']


    def test_valid_register_command(self):
        console = Console()
        def func(): return
        console.register_command('name', func, 'description')
        self.assertEqual(len(console._Console__commands), 2)
        self.assertEqual(
            [*console._Console__commands.items()][1], 
            ('name', (func, 'description'))
        )

    def test_invalid_register_command(self):
        console = Console()
        def func(): return
        self.assertRaises(
            ValueError,
            console.register_command,
            '',
            func, 
            'description'
        )

    def test_rewrite_register_command(self):
        console = Console()
        def func(): return
        console.register_command('name', func, 'description')
        def new_func(): return
        console.register_command('name', new_func, 'new_description')
        self.assertEqual(len(console._Console__commands), 2)
        self.assertEqual(
            [*console._Console__commands.items()][1], 
            ('name', (new_func, 'new_description'))
        )

    def test_print_commands(self):
        console = Console()
        def func(): return
        console.register_command('name', func, 'description')
        captured_output = io.StringIO() 
        sys.stdout = captured_output
        console.print_commands()  
        sys.stdout = sys.__stdout__  
        expected_print = 'Вы можете использовать следующие команды:\n' \
                         '\t- help: Выводит список всех доступных команд.\n' \
                         '\t- name: description\n'
        self.assertEqual(captured_output.getvalue(), expected_print)

    def test_parse_command_with_args(self):
        console = Console()
        self.assertEqual(
            console.parse_command('command a b cde 1 2'), 
            ('command', ['a', 'b', 'cde', '1', '2'])
        )

    def test_parse_command_without_args(self):
        console = Console()
        self.assertEqual(
            console.parse_command('command'), 
            ('command', [])
        )

    def test_parse_command_with_args_with_spaces(self):
        console = Console()
        self.assertEqual(
            console.parse_command('command   a b  2'), 
            ('command', ['a', 'b', '2'])
        )

    def test_parse_command_without_args_with_spaces(self):
        console = Console()
        self.assertEqual(
            console.parse_command('command   '), 
            ('command', [])
        )

    def test_parse_command_witho_args_arounded_spaces(self):
        console = Console()
        self.assertEqual(
            console.parse_command('   command   a b 2'), 
            ('command', ['a', 'b', '2'])
        )

    def test_parse_command_without_args_with_spaces_before_command(self):
        console = Console()
        self.assertEqual(
            console.parse_command('   command'), 
            ('command', [])
        )

    def test_parse_command_with_args_with_spaces_before_command(self):
        console = Console()
        self.assertEqual(
            console.parse_command('   command a b 2'), 
            ('command', ['a', 'b', '2'])
        )

    def test_parse_command_without_args_arounded_spaces(self):
        console = Console()
        self.assertEqual(
            console.parse_command('   command   '), 
            ('command', [])
        )

    def test_parse_empty_command(self):
        console = Console()
        self.assertEqual(console.parse_command(''), ('', []))

    def test_parse_empty_command_with_spaces(self):
        console = Console()
        self.assertEqual(console.parse_command('   '), ('', []))

    def test_parse_command_with_special_characters_with_args(self):
        console = Console()
        self.assertEqual(
            console.parse_command(r'command~`!@№#$%^?&*()_+-=:;\'\\/\|",. a b 2'),
            (r'command~`!@№#$%^?&*()_+-=:;\'\\/\|",.', ['a', 'b', '2'])
        )

    def test_parse_command_with_special_characters_without_args(self):
        console = Console()
        self.assertEqual(
            console.parse_command(r'command~`!@№#$%^?&*()_+-=:;\'\\/\|",.'), 
            (r'command~`!@№#$%^?&*()_+-=:;\'\\/\|",.', [])
        )

    def test_parse_command_with_special_characters_in_args(self):
        console = Console()
        self.assertEqual(
            console.parse_command(r'command ~`!@№#$%^?&*()_+-=:;\'\\/\|",. b 2'),
            ('command', [r'~`!@№#$%^?&*()_+-=:;\'\\/\|",.', 'b', '2'])
        )

    def test_valid_cast_str_to_int(self):
        console = Console()
        self.assertEqual(console.cast('int', '123'), 123)

    def test_cast_str_with_spaces_to_int(self):
        console = Console()
        self.assertEqual(console.cast('int', '123   '), 123)

    def test_invalid_cast_str_to_int(self):
        console = Console()
        self.assertRaises(ValueError, console.cast, 'int', '1a23')

    def test_valid_cast_str_to_float(self):
        console = Console()
        self.assertEqual(console.cast('float', '123.4'), 123.4)

    def test_invalid_cast_str_to_float(self):
        console = Console()
        self.assertRaises(ValueError, console.cast, 'float', '1a23.4')

    def test_cast_str_to_str(self):
        console = Console()
        self.assertEqual(
            console.cast('str', r'~`!@№#$%^   ?&*()_+-=:;\'\\/\|",.'), 
            r'~`!@№#$%^   ?&*()_+-=:;\'\\/\|",.'
        )

    def test_cast_int_to_str(self):
        console = Console()
        self.assertEqual(console.cast('str', 123), '123')

    def test_cast_float_to_str(self):
        console = Console()
        self.assertEqual(console.cast('str', 123.4), '123.4')

    def test_cast_int_to_float(self):
        console = Console()
        self.assertEqual(console.cast('float', 123), 123.)

    def test_cast_float_to_int(self):
        console = Console()
        self.assertEqual(console.cast('int', 123.4), 123)

    def test_cast_to_invalid_type(self):
        console = Console()
        self.assertEqual(console.cast('Integer64', '123'), None)

    @patch('builtins.input', return_value='unknown_command')
    @patch('itertools.count', return_value=iter([1]))
    def test_start_unknown_command(self, input_mock, itertools_count_mock):
        console = Console()
        captured_output = io.StringIO() 
        sys.stdout = captured_output
        console.start() 
        sys.stdout = sys.__stdout__  
        expected_print = 'Ошибка: неизвестная команда.\n'
        self.assertEqual(captured_output.getvalue(), expected_print)

    @patch('builtins.input', return_value='test_command')
    @patch('itertools.count', return_value=iter([1]))
    def test_start_wrong_arguments_number_1(
        self, 
        input_mock, 
        itertools_count_mock
    ):
        console = Console()
        console.register_command('test_command', lambda x: x, '')
        captured_output = io.StringIO() 
        sys.stdout = captured_output
        console.start() 
        sys.stdout = sys.__stdout__  
        expected_print = f'Ошибка: test_command принимает' \
                         f' 1 аргументов,' \
                         f' но передано 0.\n'
        self.assertEqual(captured_output.getvalue(), expected_print)

    @patch('builtins.input', return_value='test_command x y')
    @patch('itertools.count', return_value=iter([1]))
    def test_start_wrong_arguments_number_2(
        self, 
        input_mock, 
        itertools_count_mock
    ):
        console = Console()
        console.register_command('test_command', lambda x, y, z: x, '')
        captured_output = io.StringIO() 
        sys.stdout = captured_output
        console.start() 
        sys.stdout = sys.__stdout__  
        expected_print = f'Ошибка: test_command принимает' \
                         f' 3 аргументов,' \
                         f' но передано 2.\n'
        self.assertEqual(captured_output.getvalue(), expected_print)

    @patch('builtins.input', return_value='test_command arg')
    @patch('itertools.count', return_value=iter([1]))
    def test_start_wrong_argument_type_cast(
        self, 
        input_mock, 
        itertools_count_mock
    ):
        console = Console()
        def func(x: dict): return
        console.register_command('test_command', func, '')
        captured_output = io.StringIO() 
        sys.stdout = captured_output
        console.start() 
        sys.stdout = sys.__stdout__  
        expected_print = 'Ошибка: не удалось привести тип аргумента.\n'
        self.assertEqual(captured_output.getvalue(), expected_print)

    @patch('builtins.input', return_value='test_command arg')
    @patch('itertools.count', return_value=iter([1]))
    def test_start_func_without_signature_call_1(
        self, 
        input_mock, 
        itertools_count_mock
    ):
        console = Console()
        def func(x): return
        console.register_command('test_command', func, '')
        captured_output = io.StringIO() 
        sys.stdout = captured_output
        console.start() 
        sys.stdout = sys.__stdout__  
        expected_print = ''
        self.assertEqual(captured_output.getvalue(), expected_print)

    @patch('builtins.input', return_value='test_command arg')
    @patch('itertools.count', return_value=iter([1]))
    def test_start_func_without_signature_call_2(
        self, 
        input_mock, 
        itertools_count_mock
    ):
        console = Console()
        def func(x): return x - 1 
        console.register_command('test_command', func, '')
        captured_output = io.StringIO() 
        sys.stdout = captured_output
        console.start() 
        sys.stdout = sys.__stdout__  
        expected_print = 'unsupported operand type(s) for -: \'str\' and \'int\'\n'
        self.assertEqual(captured_output.getvalue(), expected_print)

    @patch('builtins.input', return_value='known_command 1 2 hello')
    @patch('itertools.count', return_value=iter([1]))
    def test_start_known_command(self, input_mock, itertools_count_mock):
        console = Console()
        def func(x: int, y: int, z: str): print(x + y, z) 
        console.register_command('known_command', func, '')
        captured_output = io.StringIO() 
        sys.stdout = captured_output
        console.start() 
        sys.stdout = sys.__stdout__  
        expected_print = '3 hello\n'
        self.assertEqual(captured_output.getvalue(), expected_print)


if __name__ == '__main__':
    unittest.main()
