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

    def help(self, user_command):
        print('CREATE table_name (column_name [INDEXED] [, ...]);')
        print('INSERT [INTO] table_name ("value" [, ...]);')
        print('SELECT FROM table_name')
        return user_command

    def create(self, user_command):
        if len(user_command.split('(')) != 2:
            return self.exception(user_command, 'There is no () or too many () in CREATE command')

        user_command_str = re.sub(r'[(),]', '', user_command)
        user_command = user_command_str.split()

        request = ['CREATE']

        table_name = user_command[1]
        if table_name in self.registered_words:
            return self.exception(user_command_str, "Table name can't be reserved word")
        request.append(table_name)
        request.append([])

        prev_word = None
        for word in user_command[2:]:
            if prev_word is not None:
                if prev_word.lower() == 'indexed' and word.lower() == 'indexed':
                    return self.exception(user_command_str)
                elif word.lower() == 'indexed':
                    request[-1].append([prev_word, 'INDEXED'])
                elif prev_word.lower() != 'indexed':
                    request[-1].append([prev_word])
            prev_word = word
        request[-1].append([prev_word])
        return request  # -> CREATE table_name [[colname, INDEXED], [colname], [...]]

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
        text = f"Command {user_command} is not supported!\nExplaining: {explain}"
        print(text)
        return text

    def parse_input(self, command):
        command = re.sub(r'[^\w\s(),=><]', '', command)     # remove non-words
        # print(command)
        command_to_parse = self.dict.get(command.split()[0].lower(), self.exception)
        return command_to_parse(command)


if __name__ == "__main__":
    parser = InputParser()
    print(parser.parse_input('INSERT table_name (value1, value2);'))
    parser.parse_input('Hello from hell kids;')
    print(parser.parse_input('CREATE shit (name is shit, kiss INDEXED my ass);'))
    print(parser.parse_input('SELECT FROM shit WHERE name = shit AND age < 10 OR name = Heavy;'))
