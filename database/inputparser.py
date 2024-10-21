# CREATE table_name (column_name [INDEXED] [, ...]);
# INSERT [INTO] table_name (“value” [, ...]);
# SELECT FROM table_name
import re


# RESERVED_COMMANDS = ['CREATE', 'INDEXED', 'INSERT', 'INTO', 'SELECT', 'FROM', 'WHERE']


class InputParser:

    def to_single_line(row_data) -> str: 
        res = ''
        if(isinstance(row_data, list)):
            for row in row_data:
                res += ' '+row
        return res


    def parse_input(data): #TODO: fix multiple command input
        command = InputParser.to_single_line(data) # parse multiple-line input
        command = re.sub(r'[^\w\s]', '', command)     # remove non-words
        command = command.split()
        if(command[0] == 'CREATE'):
            try:
                request = ['CREATE']
                for word in command[1:]:
                    if(len(request) == 1 and word !='INDEXED'):
                        request.append(word) # add name of table
                        request.append([])   # for table columns
                    elif(not word == 'INDEXED'):
                        request[-1].append([word]) # new column
                    else:
                        request[-1][-1].append('INDEXED')
                return request # -> CREATE table_name [[colname, INDEXED], [colname], [...]]
            except:
                print('such CREATE command structure is not supported')
        if(command[0] == 'INSERT'):
            try:
                request = ['INSERT']
                for word in command[1:]:
                    if(word == 'INTO'):
                        pass
                    elif(len(request) == 1):
                        request.append(word) # add name of insertion table
                        request.append([])
                    else:
                        request[-1].append(word) # append insertion column value

                return request # -> INSERT [INTO] table_name [input1, input2, ...]
            except:
                print('such INSERT command structure is not supported')