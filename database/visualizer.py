from .db import Table

class Visualizer:

    _CHARACTERS_LIMIT = 48

    def __init__(self, response):
        self.response = response
        self.response_type = type(response)

    def _create_balanced_spaces_text(self, text, data, max_lengths):
        for column_index in range(len(self.response.columns)):
            overflow = False
            length = len(data[column_index])
            if length > self._CHARACTERS_LIMIT:
                overflow = True
                length = self._CHARACTERS_LIMIT - 4
            start = (max_lengths[column_index] - length)//2
            if overflow:
                data_name = data[column_index][:length-11] + f' ... (+{len(data[column_index])-length+11})'
            else:
                data_name = data[column_index]
            name = " " * start + data_name + " " * (max_lengths[column_index] - len(data_name) - start)
            text += "|" + name
        return text

    def visualize(self):
        if self.response_type == Table:
            if self.response.data == []:
                print('TABLE IS EMPTY')
            else:
                max_lengths = {column: len(self.response.columns[column]) + 4 for column in range(len(self.response.columns))}
                for row in self.response.data:
                    for column in range(len(self.response.columns)):
                        if len(row[column]) + 4 > max_lengths[column]:
                            if len(row[column]) + 4 > self._CHARACTERS_LIMIT:
                                max_lengths[column] = self._CHARACTERS_LIMIT
                            else:
                                max_lengths[column] = len(row[column]) + 4
                sum_lengths = sum(max_lengths.values())
                splitter = '-' * (sum_lengths + len(self.response.columns) + 1) + '\n'
                text = splitter
                overflow = False
                length = len(self.response.table_name)
                if length > self._CHARACTERS_LIMIT:
                    overflow = True
                    length = self._CHARACTERS_LIMIT - 4
                start = (sum_lengths - length)//2
                if overflow:
                    data_name = self.response.table_name[:length-11] + f' ... (+{len(self.response.table_name)-length+11})'
                else:
                    data_name = self.response.table_name
                name = " " * start + data_name + " " * (sum_lengths + 2 - len(data_name) - start)
                text += "|" + name
                text += '|\n'
                text += splitter
                text = self._create_balanced_spaces_text(text, self.response.columns, max_lengths)
                text += '|\n'
                text += splitter
                for row in self.response.data:
                    text = self._create_balanced_spaces_text(text, row, max_lengths)
                    text += '|\n'
                text += splitter
                print(text)
        else:
            print(self.response)