
import pandas as pd
import numpy as np
from django.conf import settings
from datetime import datetime as dt
from datetime import timedelta

from coviddb.models import *

def getNumByAge(conn, col, group):
    df = pd.read_sql_query \
        ('SELECT %s, %s, COUNT(%s) FROM %s GROUP BY %s, %s order by %s' %
            (group, col, col, settings.INFECTED_LIST_TABLE_NAME, group, col, col), conn)

    data = []

    start = dt.strptime("2020/01/15", '%Y/%m/%d')  # 開始日
    end = dt.now()

    label = list(map(lambda x, y=start: (y + timedelta(days=x)).strftime("%Y/%m/%d"), range((end - start).days + 1)))

    color = settings.CHART_COLOR

    for age in np.arange(0, 10):
        age_list = []
        for d in label:
            inf_num = df[df[col] == d][df['age'] == age*10]['COUNT(%s)' % col].values
            if len(inf_num) > 0:
                age_list.append(inf_num[0])
            else:
                age_list.append(0)
        data.append([age*10, age_list, color[age]])

    return label, data

def getNumByState(conn, col, group):

    df = pd.read_sql_query \
        ('SELECT %s, %s, COUNT(%s) FROM %s GROUP BY %s, %s order by %s' %
            (group, col, col, settings.INFECTED_LIST_TABLE_NAME, group, col, col), conn)

    nlist = []

    # 日付条件の設定
    start = dt.strptime("2020/01/15", '%Y/%m/%d')  # 開始日
    end = dt.now()

    states = State.objects.values_list('romam', 'jp', 'color').filter(disp=1)

    datelist = list(map(lambda x, y=start: (y + timedelta(days=x)).strftime("%Y/%m/%d"), range((end - start).days + 1)))

    for ro, jp, co in states:
        sdf = df[df[group] == ro]
        lst = []
        for d in datelist:
            infnum = sdf[sdf[col] == d]['COUNT(%s)' % col].values
            if len(infnum) > 0:
                lst.append(int(infnum[0]))
            else:
                lst.append(0)
        nlist.append([jp, lst, co])

    return datelist, nlist