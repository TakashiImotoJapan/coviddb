from django.shortcuts import render
import sqlite3
import datetime
import pandas as pd
from operator import itemgetter
from django.conf import settings
from datetime import datetime as dt
from datetime import timedelta
from coviddb.util import stateutil

from coviddb.models import *

def index(request):
    numbers = JapanInfectedNumber.objects.values_list('state', 'death', 'discharge', 'hospitalization', 'positive', 'state_id')
    df = pd.DataFrame(numbers).iloc[:,:5]
    amount = [sum(df.iloc[:,1]), sum(df.iloc[:,2]), sum(df.iloc[:,3]), sum(df.iloc[:,4])]
    df.columns = settings.INFECTED_NUM_HEADER_NAME
    inf_table = df.to_html(index=False, escape=False, table_id='data_table', classes='table table-sm table-striped')

    conn = sqlite3.connect(settings.DB_PATH)
    df_age = pd.read_sql_query('SELECT age, COUNT(age) FROM %s GROUP BY age having age <= 90 order by age' % (settings.INFECTED_LIST_TABLE_NAME), conn)
    df_age['COUNT(age)'] = df_age['COUNT(age)'] * 100 / sum(df_age['COUNT(age)'])
    conn.close()

    context = {
        'AMOUNT': amount,
        'JP_INFECT_NUMBER': list(numbers),
        'INFECTED_NUMBER_LIST': inf_table,
        'AGE_PAR': list(df_age['COUNT(age)'])
    }

    return render(request, 'index.html', context)

def data(request, state):
    conn = sqlite3.connect(settings.DB_PATH)
    col = itemgetter(*settings.INFECTED_LIST_SIMPLE_COLUMN_INDEX)(settings.INFECTED_LIST_COLUMN_NAME)

    df = pd.read_sql_query('SELECT %s FROM %s where state = \'%s\'' % (",".join(col), settings.INFECTED_LIST_TABLE_NAME, state), conn)
    df.replace([None], '', inplace=True)
    df['id'] = df['id'].apply(lambda x: '<a href="/data/{1}/{0}">{0}</a>'.format(x, state))
    df['sex'] = df['sex'].replace(settings.SEX_DIC)
    df['state'] = df['state'].replace(dict(State.objects.values_list('romam', 'jp')))
    df = df.rename(columns=settings.INFECTED_LIST_HEADER_DICT)
    conn.close()
    table = df.to_html(index=False, escape=False, table_id='data_table', classes='table table-bordered table-striped')
    context = {'INFECTED_LIST': table}

    return render(request, 'data.html', context)

def detail(request, state, id):

    conn = sqlite3.connect(settings.DB_PATH)

    df = pd.read_sql_query('SELECT * FROM %s where state = \'%s\' and id = \'%s\'' % (settings.INFECTED_LIST_TABLE_NAME, state, id), conn)
    df.replace([None], '', inplace=True)
    df['full_presentation'] = df['full_presentation'].str.replace('\n', '<br>')
    df = df.rename(columns=settings.INFECTED_LIST_HEADER_DICT)
    df.index = ['データ']
    print(df.head())
    conn.close()

    table = df.transpose().to_html(escape=False, table_id='data_table', classes='table table-bordered table-striped')
    context = {'INFECTED_DATA': table}

    return render(request, 'detail.html', context)

def num_patients(request):

    conn = sqlite3.connect(settings.DB_PATH)
    datelist, inf_list = stateutil.getNumByState(conn, 'infected_date')
    datelist, ann_list = stateutil.getNumByState(conn, 'announce_date')
    conn.close()

    context = {'CHART_LABEL': datelist, 'INFECTED_NUM': inf_list, 'ANNOUNCE_NUM': ann_list}

    return render(request, 'patients.html', context)

def about(request):
    return render(request, 'about.html')

def info(request):
    return render(request, 'info.html')

def about_data(request):
    return render(request, 'about_data.html')

def data_link(request):
    return render(request, 'data_link.html')

def checkdate(s):
    date_format = '%Y/%M/%d'
    try:
        date_obj = datetime.datetime.strptime(s, date_format)
        return True
    except ValueError:
        return False