
import sqlite3
import pandas as pd
import sys

TABLE_NAME = "infected_list"

df = pd.read_csv('../data/tokyo.csv')

conn = sqlite3.connect('../db.sqlite3')

df.to_sql(TABLE_NAME, conn, if_exists='append', index=None)

df=pd.read_sql_query('SELECT * FROM %s' % TABLE_NAME, conn)

print(df)

conn.close()