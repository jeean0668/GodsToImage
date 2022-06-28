import matplotlib.font_manager as fm
import pandas as pd

import sqlite3

"""conn = sqlite3.connect('test.db', isolation_level=None)
c = conn.cursor()

df = pd.DataFrame(data=[[0, '10/11/12'], [1, '12/11/10']],
                  columns=['int_column', 'date_column'])

df.to_sql('test', conn)

a = pd.read_sql('SELECT int_column, date_column FROM test', conn)
print(a.head())"""

conn = sqlite3.connect("parsing/news/Islam_parsed/normal/_parsed_Islam_period_1.xlsx.db")
cursor = conn.cursor()
print("ok")

a = pd.read_sql("SELECT src FROM '_parsed_Islam_period_1.xlsx'", conn)
print("ok")
print(a.head())

