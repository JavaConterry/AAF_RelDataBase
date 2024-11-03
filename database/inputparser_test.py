import unittest

import io
from contextlib import redirect_stdout

from inputparser import InputParser


class InputParserTest(unittest.TestCase):
    parser = InputParser()

    def test_wrong_enter_command(self):
        f = io.StringIO()
        with redirect_stdout(f) as stdout:
            self.parser.parse_input('&   CREATE students (id INDEXED, name, age, sex);')
        self.assertEqual(stdout.getvalue(), """[!] Command "&   CREATE students (id INDEXED, name, age, sex)" is not supported!\n[?] Explaining: No such command\n""")

    def test_create(self):
        self.assertEqual(self.parser.parse_input('CREATE students (id INDEXED, name, age, sex);'), [["CREATE", "students"], ["id INDEXED", "name", "age", "sex"]])

    def test_create_tabulation(self):
        self.assertEqual(self.parser.parse_input('CREATE students  \n\t\r (id INDEXED, name, age, sex);'), [["CREATE", "students"], ["id INDEXED", "name", "age", "sex"]])

    def test_create_reserved_word_column(self):
        f = io.StringIO()
        with redirect_stdout(f) as stdout:
            self.parser.parse_input('CREATE students (id INDEXED, INDEXED, age, sex);')
        self.assertEqual(stdout.getvalue(), """[!] Command "CREATE students (id INDEXED, INDEXED, age, sex)" is not supported!\n[?] Explaining: Column name can't be reserved word\n""")

    def test_create_reserved_word_table_name(self):
        f = io.StringIO()
        with redirect_stdout(f) as stdout:
            self.parser.parse_input('CREATE INDEXED (id INDEXED, name, age, sex);')
        self.assertEqual(stdout.getvalue(), """[!] Command "CREATE INDEXED (id INDEXED, name, age, sex)" is not supported!\n[?] Explaining: Table name can't be reserved word\n""")

    def test_create_enter_command_overflow(self):
        f = io.StringIO()
        with redirect_stdout(f) as stdout:
            self.parser.parse_input('CREATE INTO INDEXED (id INDEXED, name, age, sex);')
        self.assertEqual(stdout.getvalue(), """[!] Command "CREATE INTO INDEXED (id INDEXED, name, age, sex)" is not supported!\n[?] Explaining: Too many arguments in CREATE command\n""")

    def test_create_enter_command_no_arguments(self):
        f = io.StringIO()
        with redirect_stdout(f) as stdout:
            self.parser.parse_input('CREATE;')
        self.assertEqual(stdout.getvalue(), """[!] Command "CREATE" is not supported!\n[?] Explaining: There is no "(" in CREATE command\n""")

    def test_create_enter_command_no_arguments_but_brackets(self):
        f = io.StringIO()
        with redirect_stdout(f) as stdout:
            self.parser.parse_input('CREATE ();')
        self.assertEqual(stdout.getvalue(), """[!] Command "CREATE ()" is not supported!\n[?] Explaining: There is no table name in CREATE command\n""")

    def test_create_not_standard_character_in_column_name(self):
        self.assertEqual(self.parser.parse_input('CREATE students (id INDEXED, &name, age, sex);'), [["CREATE", "students"], ["id INDEXED", "&name", "age", "sex"]])

    def test_create_not_standard_character_before_semicolon(self):
        f = io.StringIO()
        with redirect_stdout(f) as stdout:
            self.parser.parse_input('CREATE students (id INDEXED, name, age, sex) & ;')
        self.assertEqual(stdout.getvalue(), """[!] Command "CREATE students (id INDEXED, name, age, sex) &" is not supported!\n[?] Explaining: There is text after ")" in CREATE command\n""")

    def test_create_ignore_characters_after_semicolon(self):
        self.assertEqual(self.parser.parse_input('CREATE students (id INDEXED, name, age, sex); ;'), [["CREATE", "students"], ["id INDEXED", "name", "age", "sex"]])

    def test_create_quotes(self):  # NOT SURE HOW NEED TO WORK
        self.assertEqual(self.parser.parse_input('CREATE students (id INDEXED, "name is sheet", age, sex);'), [["CREATE", "students"], ["id INDEXED", '"name is sheet"', "age", "sex"]])

    def test_create_quotes_with_indexed(self):  # NOT SURE HOW NEED TO WORK
        self.assertEqual(self.parser.parse_input('CREATE students (id INDEXED, "name is sheet" INDEXED, age, sex);'), [["CREATE", "students"], ["id INDEXED", '"name is sheet" INDEXED', "age", "sex"]])

    def test_create_several_quotes(self):  # NOT SURE HOW NEED TO WORK
        f = io.StringIO()
        with redirect_stdout(f) as stdout:
            self.parser.parse_input('CREATE students (id INDEXED, "name is sheet" "name is John", age, sex);')
        self.assertEqual(stdout.getvalue(), """[!] Command "CREATE students (id INDEXED, "name is sheet" "name is John", age, sex)" is not supported!\n[?] Explaining: Wrong CREATE command syntax, no several quotes "" in table column name (id INDEXED, "name is sheet" "name is John", age, sex)\n""")

    def test_create_with_different_quotes(self):  # NOT SURE HOW NEED TO WORK
        f = io.StringIO()
        with redirect_stdout(f) as stdout:
            self.parser.parse_input('''CREATE students ('name "dad"');''')
        self.assertEqual(stdout.getvalue(), """[!] Command "CREATE students ('name "dad"')" is not supported!\n[?] Explaining: Wrong CREATE command syntax, no text before quotes in table column name ('name "dad"')\n""")

    def test_create_single_quotes(self):  # NOT SURE HOW NEED TO WORK
        self.assertEqual(self.parser.parse_input('CREATE students (id INDEXED, \'name is sheet\', age, sex);'), [["CREATE", "students"], ["id INDEXED", "'name is sheet'", "age", "sex"]])

    def test_create_indexed_in_first_place(self):
        f = io.StringIO()
        with redirect_stdout(f) as stdout:
            self.parser.parse_input('CREATE students (id INDEXED, INDEXED name, age, sex);')
        self.assertEqual(stdout.getvalue(), """[!] Command "CREATE students (id INDEXED, INDEXED name, age, sex)" is not supported!\n[?] Explaining: Wrong CREATE command syntax, no spaces in table column name (id INDEXED, INDEXED name, age, sex)\n""")

    def test_create_no_opened_brackets(self):
        f = io.StringIO()
        with redirect_stdout(f) as stdout:
            self.parser.parse_input('CREATE students id INDEXED, name, age, sex;')
        self.assertEqual(stdout.getvalue(), """[!] Command "CREATE students id INDEXED, name, age, sex" is not supported!\n[?] Explaining: There is no "(" in CREATE command\n""")

    def test_create_no_closed_brackets(self):
        f = io.StringIO()
        with redirect_stdout(f) as stdout:
            self.parser.parse_input('CREATE students (id INDEXED, name, age, sex;')
        self.assertEqual(stdout.getvalue(), """[!] Command "CREATE students (id INDEXED, name, age, sex" is not supported!\n[?] Explaining: There is no ")" in CREATE command\n""")

    def test_insert(self):
        self.assertEqual(self.parser.parse_input('INSERT students (1, Dave, 18, male);'), [["INSERT", "students"], ['1', "Dave", "18", "male"]])

    def test_insert_tabulation(self):
        self.assertEqual(self.parser.parse_input('CREATE students  \n\t\r (id INDEXED, name, age, sex);'), [["CREATE", "students"], ["id INDEXED", "name", "age", "sex"]])

    def test_insert_reserved_word_column(self):
        f = io.StringIO()
        with redirect_stdout(f) as stdout:
            self.parser.parse_input('INSERT students (id, INDEXED, age, sex);')
        self.assertEqual(stdout.getvalue(), """[!] Command "INSERT students (id, INDEXED, age, sex)" is not supported!\n[?] Explaining: Column name can't be reserved word\n""")

    def test_insert_reserved_word_table_name(self):
        f = io.StringIO()
        with redirect_stdout(f) as stdout:
            self.parser.parse_input('INSERT INDEXED (id, name, age, sex);')
        self.assertEqual(stdout.getvalue(), """[!] Command "INSERT INDEXED (id, name, age, sex)" is not supported!\n[?] Explaining: Table name can't be reserved word\n""")

    def test_insert_into_with_no_table_name(self):
        f = io.StringIO()
        with redirect_stdout(f) as stdout:
            self.parser.parse_input('INSERT INTO (id, name, age, sex);')
        self.assertEqual(stdout.getvalue(), """[!] Command "INSERT INTO (id, name, age, sex)" is not supported!\n[?] Explaining: There is no table name in INSERT command\n""")

    def test_insert_reserved_word_table_name_with_into(self):
        f = io.StringIO()
        with redirect_stdout(f) as stdout:
            self.parser.parse_input('INSERT INTO INDEXED (id, name, age, sex);')
        self.assertEqual(stdout.getvalue(), """[!] Command "INSERT INTO INDEXED (id, name, age, sex)" is not supported!\n[?] Explaining: Table name can't be reserved word\n""")

    def test_insert_with_column_spaces(self):
        f = io.StringIO()
        with redirect_stdout(f) as stdout:
            self.parser.parse_input('INSERT students (Dave Dave, 18, male);')
        self.assertEqual(stdout.getvalue(), """[!] Command "INSERT students (Dave Dave, 18, male)" is not supported!\n[?] Explaining: Wrong INSERT command syntax, no spaces in table column name (Dave Dave, 18, male)\n""")

    def test_insert_with_quotes(self):
        self.assertEqual(self.parser.parse_input('INSERT students ("Dave Dave", 18, male);'), [["INSERT", "students"], ['"Dave Dave"', "18", "male"]])

    def test_select(self):
        self.assertEqual(self.parser.parse_input('SELECT FROM students;'), [['SELECT', 'FROM', 'students'], []])


if __name__ == '__main__':
    unittest.main()
