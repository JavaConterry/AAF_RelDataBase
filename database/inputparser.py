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

    def help(self, user_command):
        print('CREATE table_name (column_name [INDEXED] [, ...]);')
        print('INSERT [INTO] table_name ("value" [, ...]);')
        print('SELECT FROM table_name')
        return user_command

    def create(self, user_command):
        try:
            request = ['CREATE']
            for word in user_command[1:]:
                if(len(request) == 1 and word != 'INDEXED'):
                    request.append(word) # add name of table
                    request.append([])   # for table columns
                elif(not word.lower() == 'INDEXED'.lower()):
                    request[-1].append([word]) # new column
                else:
                    request[-1][-1].append('INDEXED')
            return request # -> CREATE table_name [[colname, INDEXED], [colname], [...]]
        except:
            print('such CREATE command structure is not supported')

    def insert(self, user_command):
        try:
            request = ['INSERT']
            for word in user_command[1:]:
                if(word.lower() == 'INTO'.lower()):
                    pass
                elif(len(request) == 1):
                    request.append(word) # add name of insertion table
                    request.append([])
                else:
                    request[-1].append(word) # append insertion column value

            return request # -> INSERT [INTO] table_name [input1, input2, ...]
        except:
            print('such INSERT command structure is not supported')

    def select(self, user_command):
        try:
            request = ['SELECT']
            for word in user_command[1:]:
                if(word.lower() == 'FROM'.lower()):
                    pass
                elif(len(request) == 1):
                    request.append(word) # add name of selection table
                    request.append([])
                else:
                    request[-1].append(word) # append selection column value
            return request # -> SELECT FROM table_name [input1, input2, ...]
        except:
            print('such SELECT command structure is not supported')

    def exception(self, user_command):
        print(f"Command {user_command} is not supported")

    def parse_input(self, command):  # TODO: fix multiple command input
        # command = InputParser.to_single_line(data) # parse multiple-line input
        command = re.sub(r'[^\w\s]', '', command)     # remove non-words
        command = command.split()
        command_to_parse = self.dict.get(command[0].lower(), self.exception)
        return command_to_parse(command)


if __name__ == "__main__":
    parser = InputParser()
    print(parser.parse_input('INSERT table_name (value1 value2);'))
    print(parser.parse_input('Hello from hell kids'))
    print(parser.parse_input('CREATE shit INDEXED (name is shit, kiss INDEXED my ass)'))
