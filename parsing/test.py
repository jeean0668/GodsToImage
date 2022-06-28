import matplotlib.font_manager as fm
import pandas as pd

import sqlite3

conn = sqlite3.connect('test.db', isolation_level=None)
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS table1 (id integer PRIMARY KEY, name text, birthday text)")
c.execute("INSERT INTO table1 VALUES(1, 'LEE', '1987-00-00') ")

test_db = pd.read_sql("test.db")
print(test_db.head())