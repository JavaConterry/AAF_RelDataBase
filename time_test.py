import os
import json
import time

from database.inputparser import InputParser
from database.db import DataBase, Table
from database.visualizer import Visualizer


class Core():
    def __init__(self):
        db = DataBase()
        parser = InputParser()

        if not os.path.isfile("./settings.json"):
            json_str = """{\n  "autoload": ["drivers", "studeNts"]\n}"""
            with open("./settings.json", "w") as f:
                f.write(json_str)
        with open("./settings.json", 'r') as f:
            json_str = f.read()
        json_load = json.loads(json_str)

        print("Loading tables from settings...")
        print(db.do([["LOAD"], json_load.get('autoload')]))
        print("Done\n")

        # Welcome message
        print("Welcome to the Database!")

        main_input = input(">>> ")
        while main_input != 'exit' and main_input != '':
            while ';' not in main_input:
                ask = input(">>> ")
                main_input += ' ' + ask
                if ask == "" or ask == 'exit':
                    main_input = 'exit'
                    break
            if main_input == 'exit':
                break

            # command pipeline
            command = parser.parse_input(main_input)
            if(command[0][0] == 'SELECT'):
                result = []
                for tries in range(3):
                    start_time = time.time()
                    response = db.do(command)
                    result.append(time.time() - start_time)
                print('Execution Time: ', sum(result)/len(result))
            else:
                response = db.do(command)

            # visualised_response = Visualizer(response)
            # visualised_response.visualize()


            main_input = input(">>> ")


if __name__ == "__main__":
    core = Core()
