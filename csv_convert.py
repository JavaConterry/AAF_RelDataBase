import pandas as pd
import numpy as np
from database.db import Table
from database.visualizer import Visualizer

class CSV_converter:
    def __init__(self):
        pass
    
    def to_table(self, data_source, i_for_idexed_column, size):
        data = pd.read_csv(data_source)
        columns = data.columns.to_list()
        data_np = np.array(data)
        data = [list(map(str, row)) for row in data_np][:size]
        table = Table(data_source.split(".")[0], columns, indexed_columns=[columns[i_for_idexed_column]])
        print(table.columns)
        print(data[:3])
        table = table.equivalent_table_from_data(data)
        return table



# conv = CSV_converter()
# table = conv.to_table('example_data.csv')
# visualizer = Visualizer(table)
# visualizer.visualize()