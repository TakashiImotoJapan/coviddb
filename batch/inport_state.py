
import sqlite3
import pandas as pd
import sys

TABLE_NAME = "coviddb_state"

df = pd.read_csv('../data/csv/state-master.csv')

conn = sqlite3.connect('../db.sqlite3')

df.to_sql(TABLE_NAME, conn, if_exists='replace', index=None)

df=pd.read_sql_query('SELECT * FROM %s' % TABLE_NAME, conn)

print(df)

conn.close()