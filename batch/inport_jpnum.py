
import sqlite3
import pandas as pd
import datetime

TABLE_NAME = "coviddb_japaninfectednumber"

df = pd.read_csv('../data/csv/japan_num-data.csv')

conn = sqlite3.connect('../db.sqlite3')

states=pd.read_sql_query('SELECT * FROM coviddb_state', conn)

df = pd.merge(df, states, left_on='state', right_on='jp').sort_values('id')
df = df.rename(columns={'id': 'state_id'})
df = df.drop(["jp", "kana", "romam", "disp", "color"], axis=1)
df['date'] = datetime.datetime.now().strftime('%Y/%m/%d')
df['positive'] = df['positive'].replace(',','',regex=True).astype(int)
df['hospitalization'] = df['hospitalization'].replace(',','',regex=True).astype(int)
df['discharge'] = df['discharge'].replace(',','',regex=True).astype(int)
df['death'] = df['death'].replace(',','',regex=True).astype(int)

df.to_sql(TABLE_NAME, conn, if_exists='append', index=None)

df=pd.read_sql_query('SELECT * FROM %s' % TABLE_NAME, conn)

conn.close()