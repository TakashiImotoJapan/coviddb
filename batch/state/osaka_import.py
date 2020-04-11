
import pandas
import glob
import django
import os
import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "coviddb.settings")
django.setup()

flist = glob.glob("../../data/state/*.xlsx")

pandas.set_option('display.max_columns', 500)
pandas.set_option('display.max_rows', 500)
pandas.set_option("display.width", 500)

from coviddb.models import InfectedPerson

for f in flist:
    df = pandas.read_excel(f)

    df = df.rename(columns=lambda x: x if not 'Unnamed' in str(x) else '')
    df = df.reset_index()

    for d in df.iterrows():
        if(type(d[1][1]) == int):

            p = InfectedPerson()
            p.state = 'osaka'
            p.pat_id = d[1][1]
            p.age = d[1][2]
            p.setSexStr(d[1][3])
            p.living_city = str(d[1][4]) + str(d[1][6])
            p.occupation = job = d[1][9]
            p.infected_date = p.createDateStr(d[1][11])
            p.status = d[1][13]

            p.setCloseContact(d[1][15])

            p.remarks = d[1][18]

            print(p.to_csv())