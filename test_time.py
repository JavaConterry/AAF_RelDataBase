from database.inputparser import InputParser
from database.db import DataBase, Table
from database.visualizer import Visualizer
import time

class Core():
    def __init__(self):
        db = DataBase()
        parser = InputParser()
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
                total_time = 0
                for _ in range(2000):
                    start_time = time.time()
                    response = db.do(command)
                    duration = time.time() - start_time
                    total_time += duration

                average_time = total_time / 2000
                print('Avarage Time: ', average_time)
            else:
                response = db.do(command)
            visualised_response = Visualizer(response)
            visualised_response.visualize()


            main_input = input()


if __name__ == "__main__":
    core = Core()
