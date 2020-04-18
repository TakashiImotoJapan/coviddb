
import pandas as pd
from django.conf import settings
from coviddb.util.dateutil import getDateLabelList

from coviddb.models import *

def getNumByAge(conn, col, group):
    df = pd.read_sql_query \
        ('SELECT %s, %s, COUNT(%s) FROM %s GROUP BY %s, %s order by %s' %
            (group, col, col, settings.INFECTED_LIST_TABLE_NAME, group, col, col), conn)

    label = getDateLabelList()

    data = []

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

    states = State.objects.values_list('romam', 'jp', 'color').filter(disp=1)

    datelist = getDateLabelList()

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

def getStateTransition():

    positive_list = []
    positive_plus_list = []
    positive_per_list = []
    positive_incper_list = []
    hospitalization_list = []
    discharge_list = []
    death_list = []

    japan_trans = JapanInfectedNumber.objects.all()
    states = State.objects.values_list('id', 'romam', 'jp', 'color').filter(disp=1)

    datelist = getDateLabelList("2020/03/15")

    for id, ro, jp, co in states:
        state_trans = japan_trans.filter(state_id=id)
        temp = [[],[],[],[],[],[],[]]

        for d in datelist:
            day_num_list = state_trans.filter(date=d)
            if len(day_num_list) > 0:
                values = list(day_num_list.values_list("positive", "positive_plus", "positive_per", "hospitalization", "discharge", "death")[0])
                values = [x if x is not None else 0 for x in values]
            else:
                values = [0, 0, 0, 0, 0, 0]

            if values[0] != 0:
                values.append(values[1] / values[0])
            else:
                values.append(0)

            for i in range(7):
                temp[i].append(values[i])


        for i, data_list in enumerate([positive_list, positive_plus_list, positive_per_list, hospitalization_list, discharge_list, death_list, positive_incper_list]):
            data_list.append([jp, temp[i], co])

    return datelist, positive_list, positive_plus_list, positive_per_list, positive_incper_list, hospitalization_list, discharge_list, death_list