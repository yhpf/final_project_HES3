import vincent
import pandas as pd

url = "../HeatDataforML.csv"
tables = pd.read_csv(url)
line = vincent.Line(tables)
line.axis_titles(x='year', y='quantity')
line.legend(title='Energy Generated')

line.display()