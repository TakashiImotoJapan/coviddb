
import os

import sqlite3
import pandas as pd
import django

TABLE_NAME = "coviddb_japaninfectednumber"

import glob

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coviddb.settings')
django.setup()

from coviddb.models import State

flist = glob.glob("../data/state/state.csv")

conn = sqlite3.connect('../db.sqlite3')

cursor = conn.cursor()
sql = 'delete from %s' % TABLE_NAME
cursor.execute(sql)
conn.commit()

cursor = conn.cursor()

for f in flist:
    print(f)
    df = pd.read_csv(f)

    id_list = []

    for index, row in df.iterrows():
        id_list.append(State.objects.get(jp=row['state']).id)

    df['state_id'] = id_list

    print(df)

    df.to_sql(TABLE_NAME, conn, if_exists='append', index=None)

# df=pd.read_sql_query('SELECT * FROM %s' % TABLE_NAME, conn)
# print(df)

conn.close()