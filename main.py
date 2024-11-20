from database.inputparser import InputParser
from database.db import DataBase, Table
from database.visualizer import Visualizer


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
            response = db.do(command)
            visualised_response = Visualizer(response)
            visualised_response.visualize()

            main_input = input()


if __name__ == "__main__":
    core = Core()
