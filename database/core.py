from inputparser import InputParser
# from db import RelationalDataBase


class Core():
    def __init__(self):  # , db: 'RelationalDataBase'
        # self.db = db
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
            # print(main_input)
            text = parser.parse_input(main_input)
            print(text)
            # db.do_command(text)
            main_input = input()


if __name__ == "__main__":
    # db = RelationalDataBase()
    core = Core()  # (db)
