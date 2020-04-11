
import sqlite3
import pandas as pd

TABLE_NAME = "coviddb_infectedperson"

import glob

flist = glob.glob("../data/csv/*-data.csv")
print(flist)

conn = sqlite3.connect('../db.sqlite3')

cursor = conn.cursor()
sql = 'delete from %s' % TABLE_NAME
cursor.execute(sql)
conn.commit()

for f in flist:
    print(f)
    df = pd.read_csv(f)
    df['age'].fillna(999)
    df['sex'].fillna(2)
    df.to_sql(TABLE_NAME, conn, if_exists='append', index=None)

# df=pd.read_sql_query('SELECT * FROM %s' % TABLE_NAME, conn)
# print(df)

conn.close()