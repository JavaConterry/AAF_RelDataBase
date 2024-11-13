from btree import BTreeIndex

class Table:
    def __init__(self, table_name, columns, indexed_columns=None):
        self.table_name = table_name
        self.columns = columns
        self.data = []
        self.indexed_columns = indexed_columns
        self.column_trees = [BTreeIndex() for _ in range(len(indexed_columns))] if indexed_columns!=None else None
    
    # can be too slow, needs approvement
    def __equivalent_table_from_data(self, data):
        new_table = Table(self.table_name, self.columns, indexed_columns=self.indexed_columns)
        for data_unit in data:
            new_table.insert(data_unit)
        return new_table


    def insert(self, data):
        self.data.append(data)
        if self.indexed_columns is not None:
            for i in range(len(self.indexed_columns)):
                col = self.columns.index(self.indexed_columns[i])
                key = data[col]
                self.column_trees[i].insert(key, data)

    def aand(self, table):
        pass #TODO

    def oor(self, table):
        pass #TODO

    #TODO check
    def select(self, arguments):
        if not (isinstance(arguments[1], list) or isinstance(arguments[2], list)):
            return self.__equivalent_table_from_data(self.search(arguments[1], arguments[2], arguments[0]))
        elif isinstance(arguments[1], list) or isinstance(arguments[2], list):
            match arguments[0]:
                case "AND":
                    return self.select(arguments[1]).aand(self.select(arguments[2]))
                case "OR":
                    return self.select(arguments[1]).oor(self.select(arguments[2]))
                case _:
                    print("Unknown operator")

    def search(self, column, key, operator='='):
        if(column in self.indexed_columns):
            tree_idx = self.indexed_columns.index(column)
            return self.column_trees[tree_idx].search(key, operator)
        else:
            match(operator):
                case '=': return [data_unit for data_unit in self.data if key in data_unit]
                case '<': return [data_unit for data_unit in self.data if data_unit[self.columns.index(column)]<key]
                case '>': return [data_unit for data_unit in self.data if data_unit[self.columns.index(column)]>key]
                case _ : return


class DataBase:
    def __init__(self):
        self.tables = []

    def _findtable(self, table_name):
        for table in self.tables:
            if(table.table_name == table_name):
                return table
        return None


    def do(self, user_command):
        ### execute command -> results in response

        if(user_command[0][0]=="CREATE"):
            new_table = Table(user_command[0][1], [user_command[1][i][0] for i in range(len(user_command[1]))],
                              [user_command[1][i][0] for i in range(len(user_command[1])) if user_command[1][i][1]])
            self.tables.append(new_table)
            return 'COMMAND IS EXECUTED'
        
        elif(user_command[0][0]=="SELECT"):
            table = self._findtable(user_command[0][1])
            if(table is None):
                return 'TABLE NOT FOUND'
            else:
                # TODO : currently only temporary solution for complexity 1
                # Requires update when Parser structure is decided and recursion is required
                if(len(user_command)>1):
                    # return table.search(user_command[1][0], user_command[1][1], user_command[1][2])
                    return table.select(user_command[1])
                return f'TABLE_NAME: {table.table_name}\nTABLE_ARGUMENTS: {table.columns}\nTABLE_INDEXED_COLS: {table.indexed_columns}\nTABLE_DATA:\n{table.data}'
                
        elif(user_command[0][0]=='INSERT'):
            table = self._findtable(user_command[0][1])
            if(table is None):
                return 'TABLE NOT FOUND'
            else:
                table.insert(user_command[1])
            return 'COMMAND IS EXECUTED'