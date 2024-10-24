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
        self.registered_words = ['CREATE', 'INDEXED', 'INSERT', 'INTO', 'SELECT', 'FROM', 'WHERE']

    def _count_brackets(self, user_command):
        count_for_brackets = {'(': user_command.count('('), ')': user_command.count(')')}
        bracket_open = count_for_brackets['(']
        bracket_close = count_for_brackets[')']
        if bracket_open == 0:
            return self.exception(user_command, 'There is no "(" in CREATE command')
        elif bracket_open != 1:
            return self.exception(user_command, f'There is {bracket_open} "(" in CREATE command')
        if bracket_close == 0:
            return self.exception(user_command, 'There is no ")" in CREATE command')
        elif bracket_close != 1:
            return self.exception(user_command, f'There is {bracket_close} ")" in CREATE command')

    def _enter_command_check(self, enter_command, second_argument=None):
        if len(enter_command) == 1:
            return self.exception(enter_command, f'There is no table name in {enter_command[0]} command')
        if len(enter_command) >= 3:
            if second_argument is None:
                return self.exception(enter_command, f'Wrong {enter_command[0]} command syntax')
            elif enter_command[1] != second_argument:
                return self.exception(enter_command, f'Wrong {enter_command[0]} command syntax')

    def help(self, user_command):
        print('CREATE table_name (column_name [INDEXED] [, ...]);')
        print('INSERT [INTO] table_name ("value" [, ...]);')
        print('SELECT FROM table_name')
        return user_command

    def create(self, user_command):
        check_brackets = self._count_brackets(user_command)

        if check_brackets is not None:
            return check_brackets

        user_command_str = user_command

        command = user_command[:-1].split('(')
        enter_command, main_command = command[0].split(), command[1].split(',')

        self._enter_command_check(enter_command)

        for word_index in range(len(main_command)):
            word_list = main_command[word_index].split()
            main_command[word_index] = main_command[word_index].strip()
            if len(word_list) > 2:
                return self.exception(user_command_str, f'Wrong {enter_command[0]} command syntax, no spaces in table column name ({command[1]})')
            if len(word_list) == 2:
                if word_list[1].lower() != 'indexed':
                    return self.exception(user_command_str, f'Wrong {enter_command[0]} command syntax, no spaces in table column name ({command[1]})')
            if word_list[0].lower() in self.registered_words:
                return self.exception(user_command_str, "Column name can't be reserved word")

        return [enter_command, main_command]

    def insert(self, user_command):
        if len(user_command.split('(')) != 2:
            return self.exception(user_command, 'There is no () or too many () in INSERT command')

        user_command_str = re.sub(r'[(),]', '', user_command)
        user_command = user_command_str.split()

        request = ['INSERT']

        if user_command[1].lower() == 'into':
            user_command.pop(1)

        table_name = user_command[1]
        if table_name in self.registered_words:
            return self.exception(user_command_str, "Table name can't be reserved word")
        request.append(table_name)
        request.append([])

        values = user_command[2:]
        for word in values:
            request[-1].append(word)

        return request # -> INSERT [INTO] table_name [input1, input2, ...]

    def select(self, user_command):
        user_command_str = re.sub(r'[(),]', '', user_command)
        user_command = user_command_str.split()

        request = ['SELECT', 'FROM']

        table_name = user_command[2]
        if table_name in self.registered_words:
            return self.exception(user_command_str, "Table name can't be reserved word")
        request.append(table_name)
        # request.append("WHERE")
        request.append([])

        conditions = user_command[4:]
        length = len(conditions)

        count_for_main_operators = 0
        main_operators = []

        conditions_without_and_or = user_command[4:]
        for word in conditions_without_and_or:
            if word.lower() == 'and' or word.lower() == 'or':
                main_operators.append(word.upper())
                count_for_main_operators += 1
                conditions_without_and_or.remove(word)

        for word_index in range(len(conditions_without_and_or)//(count_for_main_operators+1)):
            request[-1].append([[conditions_without_and_or[3*word_index], conditions_without_and_or[3*word_index + 2]], conditions_without_and_or[3*word_index + 1]])
            if word_index != len(conditions_without_and_or)//(count_for_main_operators+1) - 1:
                request[-1].append(main_operators.pop(0))

        if (len(conditions_without_and_or) % (count_for_main_operators + 1)) != 0:
            return self.exception(user_command_str, f"Wrong conditions in SELECT command, length: {length}, AND or OR operators: {count_for_main_operators}")

        return request # -> SELECT FROM table_name WHERE [input1, input2, ...]

    def exception(self, user_command, explain='No such command'):
        text = f"[!] Command {user_command} is not supported!\n[?] Explaining: {explain}"
        print(text)
        return text

    def parse_input(self, command):
        # command = re.sub(r"""[^\w\s(),=><'";]""", '', command)     # remove non-words ^\w\s(),=><
        command = command.split(";")[0]
        command = (re.sub(r"""[^\w\s(),=><'"]""", '', command)).strip()
        print(command)
        command_to_parse = self.dict.get(command.split()[0].lower(), self.exception)
        return command_to_parse(command)


if __name__ == "__main__":
    parser = InputParser()
    print(parser.parse_input('CREATE students \n (id INDEXED, name, age, sex);'))
    # print(parser.parse_input('  \n  \t \r   &   CREATE students (id INDEXED, & name, age, sex) & ; & \n  \t \r      '))
    # (parser.parse_input('  \n  \t \r       CREATE students (id INDEXED, name is shit, age, sex)                  ;       sex              '))
    # (parser.parse_input('CREATE students (id INDEXED, "name is shit", age, sex);'))
    # (parser.parse_input("""CREATE students ('name "dad"');"""))
    # (parser.parse_input("CREATE students (id INDEXED, 'name is shit', age, sex);"))
    # (parser.parse_input('CREATE students (id INDEXED, INDEXED name is shit, age, sex);'))
    # (parser.parse_input('CREATE students (id INDEXED, name is shit, age, sex;'))
    # (parser.parse_input('CREATE students id INDEXED, name is shit, age, sex;'))
    print(parser.parse_input('INSERT students (Dave, 18, male);'))
    print(parser.parse_input('SELECT FROM students WHERE name = Dave AND age < 10 OR name = Heavy;'))
    parser.parse_input('Hello from hell, students;')
