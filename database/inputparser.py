# CREATE table_name (column_name [INDEXED] [, ...]);
# INSERT [INTO] table_name (“value” [, ...]);
# SELECT FROM table_name
import re


# RESERVED_COMMANDS = ['CREATE', 'INDEXED', 'INSERT', 'INTO', 'SELECT', 'FROM', 'WHERE']


class InputParser:
    def __init__(self):
        self.dict = {
            'HELP'.lower(): self.help,
            'CREATE'.lower(): self.create,
            'INSERT'.lower(): self.insert,
            'SELECT'.lower(): self.select
        }
        self.help_commands = {
            'HELP': "Show help",
            'CREATE': "CREATE table_name (column_name [INDEXED] [, ...]);",
            'INSERT': "INSERT [INTO] table_name (“value” [, ...]);",
            'SELECT': "SELECT FROM table_name [WHERE condition];"
        }
        self.registered_words = ['CREATE', 'INDEXED', 'INSERT', 'INTO', 'SELECT', 'FROM', 'WHERE']

    def _count_brackets(self, user_command):  # Worst case TC: O(5n + 6), worst case SC: O(4n+2)
        command_name = user_command.split()[0].upper()  # TC: O(2n), SC: O(n)
        count_for_brackets = {'(': user_command.count('('), ')': user_command.count(')')}  # TC: O(2n), SC: O(2n+2)
        bracket_open = count_for_brackets['(']  # TC: O(1), SC: O(1)
        bracket_close = count_for_brackets[')']  # TC: O(1), SC: O(1)
        if bracket_close == 1 and user_command.split(')')[1] != '':  # TC: O(n), SC: O(n) Two comparisons for the case when there is text after ")"
            return self.exception(user_command, f'There is text after ")" in {command_name} command')
        if bracket_open == 0:  # TC: O(1) one compare for the case when there is no "("
            return self.exception(user_command, f'There is no "(" in {command_name} command')
        elif bracket_open != 1:  # TC: O(1) one compare for the case when there is more than one "("
            return self.exception(user_command, f'There is {bracket_open} "(" in {command_name} command')
        if bracket_close == 0:  # TC: O(1) one compare for the case when there is no ")"
            return self.exception(user_command, f'There is no ")" in {command_name} command')
        elif bracket_close != 1:  # TC: O(1) one compare for the case when there is more than one ")"
            return self.exception(user_command, f'There is {bracket_close} ")" in {command_name} command')

    def _enter_command_check(self, enter_command, command_str, second_argument=None):
        length = len(enter_command)
        if re.sub(r"""[^a-zA-Z][^a-zA-Z0-9_]*""", '', "".join(enter_command)) != "".join(enter_command):
            return self.exception(command_str, f'Wrong Identifier name in {enter_command[0]} command, must be in the form [a-zA-Z][a-zA-Z0-9_]*, received error in {re.sub(r"""[a-zA-Z][a-zA-Z0-9_]*""", '', "".join(enter_command))}')
        match length:
            case 1:
                return self.exception(command_str, f'There is no table name in {enter_command[0]} command')
            case 2:
                if enter_command[1].upper() in self.registered_words and enter_command[1].upper() != second_argument:
                    return self.exception(command_str, f"Table name can't be reserved word")
                if enter_command[1].upper() == second_argument:
                    return self.exception(command_str, f'There is no table name in {enter_command[0]} command')
                return None
            case 3:
                if second_argument is None:
                    return self.exception(command_str, f'Too many arguments in {enter_command[0]} command')
                if enter_command[1].upper() != second_argument:
                    return self.exception(command_str, f'Wrong {enter_command[0]} command syntax')
                if enter_command[2].upper() in self.registered_words:
                    return self.exception(command_str, f"Table name can't be reserved word")
                return None
            case _:
                return self.exception(command_str, f'Too many arguments in {enter_command[0]} command')

    def _check_for_quotes(self, main_command, word_index, user_command_str, enter_command, command):
        if '"' in main_command[word_index]:
            word_list = main_command[word_index].split('"')
            if len(word_list) > 3:
                return self.exception(user_command_str, f'Wrong {enter_command[0]} command syntax, no several quotes "" in table column name ({command[1]})')
            if word_list[0] != '':
                return self.exception(user_command_str, f'Wrong {enter_command[0]} command syntax, no text before quotes in table column name ({command[1]})')
            word_list.pop(0)
            word_list[1] = word_list[1].strip()
        elif "'" in main_command[word_index]:
            word_list = main_command[word_index].split("'")
            if len(word_list) > 3:
                return self.exception(user_command_str, f"Wrong {enter_command[0]} command syntax, no several quotes '' in table column name ({command[1]})")
            if word_list[0] != '':
                return self.exception(user_command_str, f'Wrong {enter_command[0]} command syntax, no text before quotes in table column name ({command[1]})')
            word_list.pop(0)
            word_list[1] = word_list[1].strip()
        else:
            word_list = main_command[word_index].split()
        return word_list

    def help(self, user_command):
        help_command = user_command.split()
        if len(help_command) > 2:
            return self.exception(user_command, 'Wrong HELP command, too many arguments')
        if help_command[0].lower() == 'help' and len(help_command) == 1:
            print('Help commands:')
            print(*self.help_commands.items(), sep='\n')
        else:
            help_command_info = self.help_commands.get(help_command[1].upper(), None)
            if help_command_info is not None:
                print(help_command_info)
            else:
                self.exception(user_command, 'No such command')
        return user_command

    def create(self, user_command):
        check_brackets = self._count_brackets(user_command)

        if check_brackets is not None:
            return check_brackets

        user_command_str = user_command

        command = user_command[:-1].split('(')
        enter_command, raw_main_command = command[0].split(), command[1].split(',')

        check_enter_command = self._enter_command_check(enter_command, user_command_str)
        enter_command[0] = enter_command[0].upper()  # TC: O(n), SC: O(n)?, n = len(enter_command)

        if check_enter_command is not None:
            return check_enter_command

        # print(raw_main_command)
        main_command = []

        for column_name in raw_main_command:
            is_indexed = False
            words = column_name.split()
            # print(words)
            if len(words) > 2:
                return self.exception(user_command_str, f'Wrong {enter_command[0]} command syntax, no spaces in table column name ({command[1]})')
            if len(words) == 2:
                if words[1] != '' and words[1].upper() != 'INDEXED':
                    return self.exception(user_command_str, f'Wrong {enter_command[0]} command syntax, no spaces in table column name ({command[1]})')
                is_indexed = True
            if words[0].upper() in self.registered_words:
                return self.exception(user_command_str, "Column name can't be reserved word")

            for word in words:
                wrong_characters = re.sub(r"""[a-zA-Z][a-zA-Z0-9_]*""", '', word)
                # right_word = re.sub(r"""[^a-zA-Z]*[^a-zA-Z0-9]_""", '', word)
                # print(right_word, word, wrong_characters)
                if wrong_characters != '':
                    return self.exception(user_command_str, f'Wrong Identifier name in: {word}, must be in the form [a-zA-Z][a-zA-Z0-9_]*, received error in: {wrong_characters}')
            main_command.append([words[0], is_indexed])

        return [enter_command, main_command]

    def insert(self, user_command):
        check_brackets = self._count_brackets(user_command)

        if check_brackets is not None:
            return check_brackets

        user_command_str = user_command

        command = user_command[:-1].split('(')
        enter_command, main_command = command[0].split(), command[1].split(',')

        check_enter_command = self._enter_command_check(enter_command, user_command_str, 'INTO')

        if check_enter_command is not None:
            return check_enter_command

        if len(enter_command) == 3:
            enter_command.pop(1)

        for word_index in range(len(main_command)):
            main_command[word_index] = main_command[word_index].strip()
            word_list = self._check_for_quotes(main_command, word_index, user_command_str, enter_command, command)
            if len(word_list) >= 2:
                if word_list[1] == '':
                    word_list.pop()
                else:
                    return self.exception(user_command_str, f'Wrong {enter_command[0]} command syntax, no spaces in table column name ({command[1]})')
            if word_list[0].upper() in self.registered_words:
                return self.exception(user_command_str, "Column name can't be reserved word")

        return [enter_command, main_command]

    def select(self, user_command):
        user_command_str = user_command
        list_of_commands = user_command.split()

        if len(list_of_commands) > 3:
            if list_of_commands[3].lower() != 'where':
                return self.exception(user_command_str, f'Wrong SELECT command syntax, expected {self.help_commands["SELECT"]}')
            if len(list_of_commands) < 5:
                return self.exception(user_command_str, f'There is no WHERE condition in SELECT command')
        elif len(list_of_commands) <= 2:
            return self.exception(user_command_str, f'Wrong {user_command} command syntax, expected {self.help_commands["SELECT"]}')
        elif len(list_of_commands) == 3:
            if list_of_commands[0].lower() != 'select' or list_of_commands[1].lower() != 'from' or list_of_commands[2].upper() in self.registered_words:
                return self.exception(user_command_str, f'Wrong SELECT command syntax')

        enter_command, main_command = list_of_commands[:3], list_of_commands[4:]

        if re.sub(r"""[^a-zA-Z][^a-zA-Z0-9_]*""", '', "".join(enter_command)) != "".join(enter_command):
            return self.exception(user_command_str, f'Wrong Identifier name in {enter_command[0]} command, must be in the form [a-zA-Z][a-zA-Z0-9_]*, received error in {re.sub(r"""[a-zA-Z][a-zA-Z0-9_]*""", '', "".join(enter_command))}')

        count_for_main_operators = 0
        main_operators = []
        for word in main_command:
            if word.lower() == 'and' or word.lower() == 'or':
                main_operators.append(word.upper())
                count_for_main_operators += 1
                main_command.remove(word)

        length = len(main_command)
        if (length % (count_for_main_operators + 1)) != 0:
            return self.exception(user_command_str, f'Wrong conditions in SELECT command')

        conditions = []
        pairs_length = length//(count_for_main_operators+1)
        for word_index in range(pairs_length):
            conditions.append([[main_command[3*word_index], main_command[3*word_index + 2]], main_command[3*word_index + 1]])
            if word_index != pairs_length - 1:
                conditions.append(main_operators.pop(0))
        if main_operators:
            return self.exception(user_command_str, f'Wrong conditions in SELECT command, no continuation for {main_operators[0]} operator')

        main_command = conditions

        return [enter_command, main_command]

    def exception(self, user_command, explain='No such command'):
        text = f'[!] Command "{user_command}" is not supported!\n[?] Explaining: {explain}'
        print(text)
        return text

    def parse_input(self, command):
        command = command.split(";")[0].strip()
        # command = (re.sub(r"""[^\w\s(),=><'"]""", '', command)).strip() # remove non-words ^\w\s(),=><
        command_to_parse = self.dict.get(command.split()[0].lower(), self.exception)
        return command_to_parse(command)


if __name__ == '__main__':
    parser = InputParser()
    print(parser.parse_input("CREAte cats(id INDEXED, name INDEXED, favourite_food);"))
    # print(parser.parse_input("SELECT FROM students WHERE name = Dave"))
    # print(parser.parse_input("SELECT FROM Customers WHERE Country = 'Mexico'; "))
    # print(parser.parse_input('SELECT FROM cats WHERE name < "Murzik" OR name = "Pushok";'))
