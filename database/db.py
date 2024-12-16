
from ntpath import isfile
import os
import json

import pandas as pd

from .deprecated.btree import BTreeIndex
from .avl import AVLTree



class Table(dict):
    def __init__(self, table_name, columns, data=None, indexed_columns=None, column_trees=None):
        super().__init__()
        self.__dict__ = self
        self.table_name = table_name
        self.columns = columns
        if data is None:
            self.data = []
        else:
            self.data = data
        self.indexed_columns = indexed_columns

        if column_trees is not None:
            self.column_trees = column_trees
        else:
            self.column_trees = [AVLTree() for _ in range(len(indexed_columns))] if indexed_columns is not None else None

    @staticmethod
    def from_dict(dict_):
        node = Table(dict_['table_name'], dict_['columns'], dict_['data'], dict_['indexed_columns'], dict_['column_trees'])
        # node.column_trees = list(map(AVLTree.from_dict, node.column_trees))
        return node

    @staticmethod
    def from_csv(file_path):
        data = pd.read_csv(file_path)
        table_name = file_path.split(".")[0]

        columns = data.columns.to_list()
        indexed_columns = None
        for col_index in range(len(columns)):
            if "INDEXED" in columns[col_index].upper():
                columns[col_index] = columns[col_index].replace("INDEXED", "").strip()
                if indexed_columns is None:
                    indexed_columns = [columns[col_index]]
                else:
                    indexed_columns.append(columns[col_index])
            columns[col_index] = columns[col_index].strip()

        data = [list(map(str, row)) for row in data.values]
        table = Table(table_name, columns, indexed_columns=indexed_columns)
        for data_unit in data:
            table.insert(data_unit)
        return table


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
        intersection_data = [x for x in self.data if x in table.data]
        return self.__equivalent_table_from_data(intersection_data)

    def oor(self, table):
        union_data = []
        concat = self.data + table.data

        for x in concat:
            if x not in union_data:
                union_data.append(x)
        return self.__equivalent_table_from_data(union_data)

    def select(self, arguments):
        if (arguments == []):
            # return self.data
            return self
        if not (isinstance(arguments[1], list) or isinstance(arguments[2], list)):
            search_result = self.search(arguments[1], arguments[2], arguments[0])
            if not isinstance(search_result, list):
                return search_result
            else:
                return self.__equivalent_table_from_data(search_result)
        elif isinstance(arguments[1], list) or isinstance(arguments[2], list):
            if isinstance(arguments[1], str):
                return arguments[1]
            elif isinstance(arguments[2], str):
                return arguments[2]
            match arguments[0]:
                case "AND":
                    return self.select(arguments[1]).aand(self.select(arguments[2]))
                case "OR":
                    return self.select(arguments[1]).oor(self.select(arguments[2]))
                case _:
                    return "UNKNOWN OPERATOR"

    def search(self, column, key, operator='='):
        if (column not in self.columns):
            return f'COLUMN {column} NOT FOUND'
        if (column in self.indexed_columns):
            tree_idx = self.indexed_columns.index(column)
            return self.column_trees[tree_idx].search(key, operator)
        else:
            match(operator):
                case '=': return [data_unit for data_unit in self.data if data_unit[self.columns.index(column)] == key]
                case '<': return [data_unit for data_unit in self.data if data_unit[self.columns.index(column)] < key]
                case '>': return [data_unit for data_unit in self.data if data_unit[self.columns.index(column)] > key]
                case _: return f'WRONG OPERATOR {operator}'


class DataBase:
    def __init__(self):
        self.tables = []

    def __findtable(self, table_name):
        for table in self.tables:
            if (table.table_name == table_name):
                return table
        return None

    def do(self, user_command):
        ### execute command -> results in response

        if (user_command[0][0] == "CREATE"):
            if self.__findtable(user_command[0][1]) is None:
                new_table = Table(user_command[0][1], [user_command[1][i][0] for i in range(len(user_command[1]))], None,
                                [user_command[1][i][0] for i in range(len(user_command[1])) if user_command[1][i][1]])
                self.tables.append(new_table)
                return 'COMMAND IS EXECUTED'
            else:
                return 'TABLE ALREADY EXISTS'

        elif (user_command[0][0] == "SELECT"):
            table = self.__findtable(user_command[0][1])
            if(table is None):
                return 'TABLE NOT FOUND'
            else:
                if(len(user_command)>1):
                    return table.select(user_command[1])
                # return f'TABLE_NAME: {table.table_name}\nTABLE_ARGUMENTS: {table.columns}\nTABLE_INDEXED_COLS: {table.indexed_columns}\nTABLE_DATA:\n{table.data}'
                return table

        elif (user_command[0][0] == 'INSERT'):
            table = self.__findtable(user_command[0][1])
            if (table is None):
                return 'TABLE NOT FOUND'
            else:
                if(len(table.columns) == len(user_command[1])):
                    table.insert(user_command[1])
                else:
                    return 'WRONG NUMBER OF ARGUMENTS'
            return 'COMMAND IS EXECUTED'

        elif (user_command[0][0] == 'SAVE'):
            for table_name in user_command[1]:
                table = self.__findtable(table_name)
                if (table is None):
                    return 'TABLE NOT FOUND'
                else:
                    if not os.path.exists("./tables"):
                        os.makedirs("./tables")
                    if table.column_trees == []:
                        json_str = json.dumps(table, indent=2)
                    else:
                        table_without_column_trees = Table(table.table_name, table.columns, table.data, table.indexed_columns)
                        json_str = json.dumps(table_without_column_trees, indent=2)
                    with open("./tables/" + table_name + '.json', 'w') as f:
                        f.write(json_str)
            return 'COMMAND IS EXECUTED'

        elif (user_command[0][0] == 'LOAD'):
            for table_name in user_command[1]:
                # print("./tables/" + table_name + '.json')
                if not os.path.exists("./tables"):
                    return 'NO tables DIRECTORY'
                list_of_tables = os.listdir("./tables")
                if table_name + '.json' not in list_of_tables:
                    print('TABLE ' + table_name + ' NOT FOUND')
                else:
                    if self.__findtable(table_name) is not None:
                        print('TABLE ' + table_name + ' ALREADY EXISTS')
                        rewrite = input("Rewrite? (y/n) ")
                        if rewrite.lower() != 'y':
                            return 'COMMAND IS EXECUTED'
                    with open("./tables/" + table_name + '.json', 'r') as f:
                        json_str = f.read()
                    json_to_table = json.loads(json_str)
                    table = Table.from_dict(json_to_table)
                    ind_col = table.indexed_columns
                    if ind_col:
                        table.column_trees = [AVLTree() for _ in range(len(ind_col))]
                        for i in range(len(ind_col)):
                            for row in table.data:
                                col = table.columns.index(ind_col[i])
                                key = row[col]
                                table.column_trees[i].insert(key, row)
                    self.tables.append(table)
            return 'COMMAND IS EXECUTED'

        elif (user_command[0][0] == 'READ'):
            for csv_file in user_command[1]:
                table = Table.from_csv(csv_file)
                self.tables.append(table)
            return 'COMMAND IS EXECUTED'
