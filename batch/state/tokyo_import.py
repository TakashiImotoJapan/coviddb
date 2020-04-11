
import pandas
import glob
import django
import os
import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "coviddb.settings")
django.setup()

flist = glob.glob("../../data/state/*.csv")

pandas.set_option('display.max_columns', 500)
pandas.set_option('display.max_rows', 500)
pandas.set_option("display.width", 500)

from coviddb.models import InfectedPerson

for f in flist:
    df = pandas.read_csv(f)

    df = df.rename(columns=lambda x: x if not 'Unnamed' in str(x) else '')
    df = df.reset_index()
    print(df)

    for index, row in df.iterrows():
        if(type(row[1]) == int):
            p = InfectedPerson()
            p.state = 'tokyo'
            p.id = row[1]
            p.city_no = row[2]
            p.living_city = row[4]
            p.announce_date = p.createDateStr(row[5])
            p.infected_date = p.createDateStr(row[7])
            p.living_state = '東京都' if row[8] == '都内' else row[8]
            p.setAge(row[9])
            p.setSexStr(row[10])
            p.living_state = row[12]
            p.symptoms = row[13]
            p.travel_history = row[14]
            p.remarks = row[15]
            p.discharge = row[16]

            print(p.to_csv())
