import unittest

import io
from contextlib import redirect_stdout

from database.inputparser import InputParser


class InputParserTest(unittest.TestCase):
    parser = InputParser()

    def test_wrong_enter_command(self):
        f = io.StringIO()
        with redirect_stdout(f) as stdout:
            self.parser.parse_input('Hello from hell, students;')
        self.assertEqual(stdout.getvalue(), """[!] Command "Hello from hell, students" is not supported!\n[?] Explanation: No such command\n""")

    def test_wrong_enter_command_not_standard_character(self):
        f = io.StringIO()
        with redirect_stdout(f) as stdout:
            self.parser.parse_input('&   CREATE students (id INDEXED, name, age, sex);')
        self.assertEqual(stdout.getvalue(), """[!] Command "&   CREATE students (id INDEXED, name, age, sex)" is not supported!\n[?] Explanation: No such command\n""")

    ### CREATE ###

    def test_create(self):  # Accepted
        self.assertEqual(self.parser.parse_input('CREATE students (id INDEXED, name, age, sex);'), [["CREATE", "students"], [['id', True], ['name', False], ['age', False], ['sex', False]]])

    def test_create_tabulation(self):  # Accepted
        self.assertEqual(self.parser.parse_input('CREATE students  \n\t\r (id INDEXED, name, age, sex)\n\t\r ; \n\t\r '), [["CREATE", "students"], [['id', True], ['name', False], ['age', False], ['sex', False]]])

    def test_create_ignore_characters_after_semicolon(self):  # Accepted
        self.assertEqual(self.parser.parse_input('CREATE students (id INDEXED, name, age, sex); ;'), [["CREATE", "students"], [['id', True], ['name', False], ['age', False], ['sex', False]]])

    def test_create_reserved_word_column(self):
        f = io.StringIO()
        with redirect_stdout(f) as stdout:
            self.parser.parse_input('CREATE students (id INDEXED, INDEXED, age, sex);')
        self.assertEqual(stdout.getvalue(), """[!] Command "CREATE students (id INDEXED, INDEXED, age, sex)" is not supported!\n[?] Explanation: Column name can't be reserved word\n""")

    def test_create_reserved_word_table_name(self):
        f = io.StringIO()
        with redirect_stdout(f) as stdout:
            self.parser.parse_input('CREATE INDEXED (id INDEXED, name, age, sex);')
        self.assertEqual(stdout.getvalue(), """[!] Command "CREATE INDEXED (id INDEXED, name, age, sex)" is not supported!\n[?] Explanation: Table name can't be reserved word\n""")

    def test_create_enter_command_overflow(self):
        f = io.StringIO()
        with redirect_stdout(f) as stdout:
            self.parser.parse_input('CREATE INTO INDEXED (id INDEXED, name, age, sex);')
        self.assertEqual(stdout.getvalue(), """[!] Command "CREATE INTO INDEXED (id INDEXED, name, age, sex)" is not supported!\n[?] Explanation: Too many arguments in CREATE command\n""")

    def test_create_enter_command_no_arguments(self):
        f = io.StringIO()
        with redirect_stdout(f) as stdout:
            self.parser.parse_input('CREATE;')
        self.assertEqual(stdout.getvalue(), """[!] Command "CREATE" is not supported!\n[?] Explanation: There is no "(" in CREATE command\n""")

    def test_create_enter_command_no_arguments_but_brackets(self):
        f = io.StringIO()
        with redirect_stdout(f) as stdout:
            self.parser.parse_input('CREATE ();')
        self.assertEqual(stdout.getvalue(), """[!] Command "CREATE ()" is not supported!\n[?] Explanation: There is no table name in CREATE command\n""")

    def test_create_not_standard_character_in_column_name(self):
        f = io.StringIO()
        with redirect_stdout(f) as stdout:
            self.parser.parse_input('CREATE students (id INDEXED, &name, age, sex);')
        self.assertEqual(stdout.getvalue(), """[!] Command "CREATE students (id INDEXED, &name, age, sex)" is not supported!\n[?] Explanation: Wrong Identifier name in: &name, must be in the form [a-zA-Z][a-zA-Z0-9_]*, received error in: &\n""")

    def test_create_non_ascii_character_in_table_name(self):
        f = io.StringIO()
        with redirect_stdout(f) as stdout:
            self.parser.parse_input('CREATE \05students (id INDEXED, name, age, sex);')
        self.assertEqual(stdout.getvalue(), """[!] Command "CREATE \05students (id INDEXED, name, age, sex)" is not supported!\n[?] Explanation: Wrong Identifier name in CREATE command, must be in the form [a-zA-Z][a-zA-Z0-9_]*, received error in \05\n""")

    def test_create_non_ascii_character_in_column_name(self):
        f = io.StringIO()
        with redirect_stdout(f) as stdout:
            self.parser.parse_input('CREATE students (id INDEXED, \05name, age, sex);')
        self.assertEqual(stdout.getvalue(), """[!] Command "CREATE students (id INDEXED, \05name, age, sex)" is not supported!\n[?] Explanation: Wrong Identifier name in: \05name, must be in the form [a-zA-Z][a-zA-Z0-9_]*, received error in: \05\n""")

    def test_create_not_standard_character_before_semicolon(self):
        f = io.StringIO()
        with redirect_stdout(f) as stdout:
            self.parser.parse_input('CREATE students (id INDEXED, name, age, sex) & ;')
        self.assertEqual(stdout.getvalue(), """[!] Command "CREATE students (id INDEXED, name, age, sex) &" is not supported!\n[?] Explanation: There is text after ")" in CREATE command\n""")

    def test_create_quotes(self):
        f = io.StringIO()
        with redirect_stdout(f) as stdout:
            self.parser.parse_input('CREATE students (id INDEXED, "name is sheet", age, sex);')
        self.assertEqual(stdout.getvalue(), """[!] Command "CREATE students (id INDEXED, "name is sheet", age, sex)" is not supported!\n[?] Explanation: Wrong CREATE command syntax, no spaces in table column name (id INDEXED, "name is sheet", age, sex)\n""")

    def test_create_quotes_with_indexed(self):
        f = io.StringIO()
        with redirect_stdout(f) as stdout:
            self.parser.parse_input('CREATE students (id INDEXED, "name is sheet" INDEXED, age, sex);')
        self.assertEqual(stdout.getvalue(), """[!] Command "CREATE students (id INDEXED, "name is sheet" INDEXED, age, sex)" is not supported!\n[?] Explanation: Wrong CREATE command syntax, no spaces in table column name (id INDEXED, "name is sheet" INDEXED, age, sex)\n""")

    def test_create_several_quotes(self):
        f = io.StringIO()
        with redirect_stdout(f) as stdout:
            self.parser.parse_input('CREATE students (id INDEXED, "name is sheet" "name is John", age, sex);')
        self.assertEqual(stdout.getvalue(), """[!] Command "CREATE students (id INDEXED, "name is sheet" "name is John", age, sex)" is not supported!\n[?] Explanation: Wrong CREATE command syntax, no spaces in table column name (id INDEXED, "name is sheet" "name is John", age, sex)\n""")

    def test_create_with_different_quotes(self):
        f = io.StringIO()
        with redirect_stdout(f) as stdout:
            self.parser.parse_input('''CREATE students ('name "dad"');''')
        self.assertEqual(stdout.getvalue(), """[!] Command "CREATE students ('name "dad"')" is not supported!\n[?] Explanation: Wrong CREATE command syntax, no spaces in table column name ('name "dad"')\n""")

    def test_create_single_quotes(self):
        f = io.StringIO()
        with redirect_stdout(f) as stdout:
            self.parser.parse_input('CREATE students (id INDEXED, \'name is sheet\', age, sex);')
        self.assertEqual(stdout.getvalue(), """[!] Command "CREATE students (id INDEXED, 'name is sheet', age, sex)" is not supported!\n[?] Explanation: Wrong CREATE command syntax, no spaces in table column name (id INDEXED, 'name is sheet', age, sex)\n""")

    def test_create_with_quotes(self):
        f = io.StringIO()
        with redirect_stdout(f) as stdout:
            self.parser.parse_input('CREATE "dad students" (id INDEXED, name, age, sex);')
        self.assertEqual(stdout.getvalue(), """[!] Command "CREATE "dad students" (id INDEXED, name, age, sex)" is not supported!\n[?] Explanation: Wrong Identifier name in CREATE command, must be in the form [a-zA-Z][a-zA-Z0-9_]*, received error in ""\n""")

    def test_create_indexed_in_first_place(self):
        f = io.StringIO()
        with redirect_stdout(f) as stdout:
            self.parser.parse_input('CREATE students (id INDEXED, INDEXED name, age, sex);')
        self.assertEqual(stdout.getvalue(), """[!] Command "CREATE students (id INDEXED, INDEXED name, age, sex)" is not supported!\n[?] Explanation: Wrong CREATE command syntax, no spaces in table column name (id INDEXED, INDEXED name, age, sex)\n""")

    def test_create_no_opened_brackets(self):
        f = io.StringIO()
        with redirect_stdout(f) as stdout:
            self.parser.parse_input('CREATE students id INDEXED, name, age, sex;')
        self.assertEqual(stdout.getvalue(), """[!] Command "CREATE students id INDEXED, name, age, sex" is not supported!\n[?] Explanation: There is no "(" in CREATE command\n""")

    def test_create_no_closed_brackets(self):
        f = io.StringIO()
        with redirect_stdout(f) as stdout:
            self.parser.parse_input('CREATE students (id INDEXED, name, age, sex;')
        self.assertEqual(stdout.getvalue(), """[!] Command "CREATE students (id INDEXED, name, age, sex" is not supported!\n[?] Explanation: There is no ")" in CREATE command\n""")

    ### INSERT ###

    def test_insert(self):  # Accepted
        self.assertEqual(self.parser.parse_input('INSERT INTO cats ("1", "Murzik", "Sausages");'), [["INSERT", "cats"], ['1', "Murzik", "Sausages"]])
        # self.assertEqual(self.parser.parse_input('INSERT students (1, Dave, 18, male);'), [["INSERT", "students"], ['1', "Dave", "18", "male"]])

    def test_insert_tabulation(self):  # Accepted
        self.assertEqual(self.parser.parse_input('INSERT INTO cats \n\t\r ("1", "Murzik", "Sausages")\n\t\r ;\n\t\r '), [["INSERT", "cats"], ['1', "Murzik", "Sausages"]])

    def test_insert_reserved_word_table_name(self):
        f = io.StringIO()
        with redirect_stdout(f) as stdout:
            self.parser.parse_input('INSERT INDEXED (id, name, age, sex);')
        self.assertEqual(stdout.getvalue(), """[!] Command "INSERT INDEXED (id, name, age, sex)" is not supported!\n[?] Explanation: Table name can't be reserved word\n""")

    def test_insert_into_with_no_table_name(self):
        f = io.StringIO()
        with redirect_stdout(f) as stdout:
            self.parser.parse_input('INSERT INTO (id, name, age, sex);')
        self.assertEqual(stdout.getvalue(), """[!] Command "INSERT INTO (id, name, age, sex)" is not supported!\n[?] Explanation: There is no table name in INSERT command\n""")

    def test_insert_reserved_word_table_name_with_into(self):
        f = io.StringIO()
        with redirect_stdout(f) as stdout:
            self.parser.parse_input('INSERT INTO INDEXED (id, name, age, sex);')
        self.assertEqual(stdout.getvalue(), """[!] Command "INSERT INTO INDEXED (id, name, age, sex)" is not supported!\n[?] Explanation: Table name can't be reserved word\n""")

    def test_insert_without_quotes(self):
        f = io.StringIO()
        with redirect_stdout(f) as stdout:
            self.parser.parse_input('INSERT students (Dave Dave, 18, male);')
        self.assertEqual(stdout.getvalue(), """[!] Command "INSERT students (Dave Dave, 18, male)" is not supported!\n[?] Explanation: Wrong INSERT command syntax, too few quotes in table column name: Dave Dave\n""")

    def test_insert_with_quotes_in_table_name(self):
        f = io.StringIO()
        with redirect_stdout(f) as stdout:
            self.parser.parse_input('INSERT "students" (id, name, age, sex);')
        self.assertEqual(stdout.getvalue(), """[!] Command "INSERT "students" (id, name, age, sex)" is not supported!\n[?] Explanation: Wrong Identifier name in INSERT command, must be in the form [a-zA-Z][a-zA-Z0-9_]*, received error in ""\n""")

    ### SELECT ###

    def test_select(self):  # Accepted
        self.assertEqual(self.parser.parse_input('SELECT FROM students;'), [['SELECT', 'students'], []])

    def test_wrong_select(self):
        f = io.StringIO()
        with redirect_stdout(f) as stdout:
            self.parser.parse_input('SELECT dad students;')
        self.assertEqual(stdout.getvalue(), """[!] Command "SELECT dad students" is not supported!\n[?] Explanation: Wrong SELECT command syntax, expected SELECT FROM table_name [WHERE condition];\n""")

    def test_wrong_select_where(self):
        f = io.StringIO()
        with redirect_stdout(f) as stdout:
            self.parser.parse_input('SELECT From students where;')
        self.assertEqual(stdout.getvalue(), """[!] Command "SELECT From students where" is not supported!\n[?] Explanation: Wrong SELECT command syntax, too few arguments with WHERE\n""")

    def test_select_where(self):  # Accepted
        self.assertEqual(self.parser.parse_input('SELECT FROM students WHERE ((name = "Dave") AND (age < "10")) OR (name = "Heavy");'), [['SELECT', 'students'], ['OR', ['AND', ['=', 'name', 'Dave'], ['<', 'age', '10']], ['=', 'name', 'Heavy']]])

    def test_select_where_big(self):  # Accepted
        self.assertEqual(self.parser.parse_input('SELECT FROM cats WHERE (((name < "Murzik") OR (name = "Pushok")) OR (name < "Pavlik")) OR ((name < "Murzik") OR (name = "Pushok"));'), [['SELECT', 'cats'], ['OR', ['OR', ['OR', ['<', 'name', 'Murzik'], ['=', 'name', 'Pushok']], ['<', 'name', 'Pavlik']], ['OR', ['<', 'name', 'Murzik'], ['=', 'name', 'Pushok']]]])

    def test_select_no_continuation(self):
        f = io.StringIO()
        with redirect_stdout(f) as stdout:
            self.parser.parse_input('SELECT FROM students WHERE ((name = "Dave") AND (age < "10")) OR;')
        self.assertEqual(stdout.getvalue(), """[!] Command "SELECT FROM students WHERE ((name = "Dave") AND (age < "10")) OR" is not supported!\n[?] Explanation: Wrong SELECT command syntax, expected SELECT FROM table_name [WHERE condition];\n[?] condition := column_name operator “value” | (condition) AND/OR (condition) | operator  := ( = | < )\n[-] Received: [[['name = "Dave"'], ' AND ', ['age < "10"']], ' OR']\n""")

    def test_select_wrong_condition_one_len(self):
        f = io.StringIO()
        with redirect_stdout(f) as stdout:
            self.parser.parse_input('SELECT FROM students WHERE ((name = "Dave") AND (age < "10")) AND (name);')
        self.assertEqual(stdout.getvalue(), """[!] Command "SELECT FROM students WHERE ((name = "Dave") AND (age < "10")) AND (name)" is not supported!\n[?] Explanation: [?] Wrong SELECT command syntax, too few quotes in table column name: name\n""")

    def test_select_wrong_condition_two_len(self):
        self.maxDiff = None
        f = io.StringIO()
        with redirect_stdout(f) as stdout:
            self.parser.parse_input('SELECT FROM students WHERE ((name = "Don") AND (age < "25")) AND (name =);')
        self.assertEqual(stdout.getvalue(), """[!] Command "SELECT FROM students WHERE ((name = "Don") AND (age < "25")) AND (name =)" is not supported!\n[?] Explanation: [?] Wrong SELECT command syntax, too few quotes in table column name: name\n[?] Wrong SELECT command syntax, too few quotes in table column name: name =\n""")

    def test_select_with_quotes(self):
        f = io.StringIO()
        with redirect_stdout(f) as stdout:
            self.parser.parse_input('SELECT FROM "students";')
        self.assertEqual(stdout.getvalue(), """[!] Command "SELECT FROM "students"" is not supported!\n[?] Explanation: Wrong Identifier name in: "students", must be in the form [a-zA-Z][a-zA-Z0-9_]*, received error in: ""\n""")

    def test_select_with_no_table_name(self):
        f = io.StringIO()
        with redirect_stdout(f) as stdout:
            self.parser.parse_input('SELECT FROM ;')
        self.assertEqual(stdout.getvalue(), """[!] Command "SELECT FROM" is not supported!\n[?] Explanation: Wrong SELECT command syntax, too few arguments\n""")


if __name__ == '__main__':
    unittest.main()
