from inputparser import InputParser


class DataUnit:
    def __init__(self, data=[]):
        self.data = data


class RelationalDataBase:
    def __init__(self):
        self.add_data(DataUnit()) # Initial db structure to be restructured


    def read_input(self, console_mode=True):
        if(console_mode):
            input_data_rows = []
            inp = 1
            while(inp != ''):
                inp = input()
                input_data_rows.append(inp)
            self.add_data(self, InputParser.parse_input(input_data_rows))
        

    def add_data(self, data :DataUnit):
        self.data.append(data)