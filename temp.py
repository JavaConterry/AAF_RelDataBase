import pandas as pd

df = pd.read_csv('chicago-ridesharing-vehicles.csv')
# df['MAKE_ni'] = df['MAKE']
# df.to_csv('example_data.csv', index=False)

print(df[df['MAKE']  == 'Jeep'].count)