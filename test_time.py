from database.inputparser import InputParser
from database.db import DataBase
from database.visualizer import Visualizer
from csv_convert import CSV_converter
import time

class Core():
    def __init__(self):
        db = DataBase()
        parser = InputParser()
        converter = CSV_converter()

        indexed = 3
        csv_table = converter.to_table('example_data.csv', indexed, size=100000)
        db.tables.append(csv_table)
        print(f'CSV was successfuly converted to table {csv_table.table_name}, with btree in column {indexed, csv_table.columns[indexed]}')
        print(f'Given columns {csv_table.columns}')
        print(f'Table indexed columns {csv_table.indexed_columns}')
        print(f'Table size {len(csv_table.data)}')
        print(f'Data in Tree: {csv_table.column_trees[0].total_data_length()}')
        main_input = input()
        while main_input != 'exit' and main_input != '':
            while ';' not in main_input:
                ask = input()
                main_input += ' ' + ask
                if ask == "" or ask == 'exit':
                    main_input = 'exit'
                    break
            if main_input == 'exit':
                break
            
            
            # command pipeline
            command = parser.parse_input(main_input)
            if(command[0][0] == 'SELECT'):
                start_time = time.time()
                response = db.do(command)
            else:
                response = db.do(command)
            visualised_response = Visualizer(response)
            visualised_response.visualize()
            print('Execution Time: ', time.time() - start_time)
            print('Result size: ', response.column_trees[0].total_data_length())


            main_input = input()


if __name__ == "__main__":
    core = Core()
