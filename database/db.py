from inputparser import InputParser


class DataUnit:
    def __init__(self, data=[]):
        self.data = data


class Table:
    def __init__(self, table_name, columns):
        self.table_name = table_name
        self.columns = columns
    
    # def create_table()


class DataBase:
    def __init__(self):
        self.tables = []


    def do(self, user_command):
        ### execute command -> results in response

        if(user_command[0][0]=="CREATE"):
            new_table = Table(user_command[0][1], user_command[1])
            self.tables.append(new_table)
            return 'COMMAND IS EXECUTED'
        
        elif(user_command[0][0]=="SELECT"):
            for table in self.tables:
                if(table.table_name == user_command[0][2]):
                    return f'TABLE_NAME: {table.table_name}\n TABLE_ARGUMENTS: {table.columns}'