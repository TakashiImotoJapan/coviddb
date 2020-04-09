
import pandas as pd
from django.conf import settings
from datetime import datetime as dt
from datetime import timedelta

from coviddb.models import *

def getNumByState(conn, col):

    df = pd.read_sql_query \
        ('SELECT state, %s, COUNT(%s) FROM %s GROUP BY state, %s order by %s' %
            (col, col, settings.INFECTED_LIST_TABLE_NAME, col, col), conn)

    nlist = []

    # 日付条件の設定
    start = dt.strptime("2020/01/15", '%Y/%m/%d')  # 開始日
    end = dt.strptime("2020/04/04", '%Y/%m/%d')  # 終了日

    states = State.objects.values_list('romam', 'jp', 'color').filter(disp=1)

    datelist = list(map(lambda x, y=start: (y + timedelta(days=x)).strftime("%Y/%m/%d"), range((end - start).days + 1)))

    for ro, jp, co in states:
        sdf = df[df['state'] == ro]
        lst = []
        for d in datelist:
            infnum = sdf[sdf[col] == d]['COUNT(%s)' % col].values
            if len(infnum) > 0:
                lst.append(int(infnum[0]))
            else:
                lst.append(0)
        nlist.append([jp, lst, co])

    return datelist, nlist