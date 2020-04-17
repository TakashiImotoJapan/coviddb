from django.shortcuts import render
import sqlite3
import pandas as pd
from operator import itemgetter
from django.conf import settings
from coviddb.util import stateutil
from django.db.models import Count
from coviddb.util.dateutil import getDateLabelList

from coviddb.models import *
from django.db.models import Count, Max

def index(request):
    numbers = JapanInfectedNumber.objects.values_list('state', 'positive', 'hospitalization', 'discharge', 'death', 'positive_plus', 'positive_per', 'state_id', 'date').order_by('date').reverse()
    numbers = numbers.filter(date=numbers[0][8]).order_by('positive')

    date = numbers[0][8].split('/')

    df = pd.DataFrame(numbers)
    df = df.iloc[:,:5]

    amount = [sum(df.iloc[:,1]), sum(df.iloc[:,2]), sum(df.iloc[:,3]), sum(df.iloc[:,4]), sum(pd.DataFrame(numbers).iloc[:,5])]
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
        'LAST_UPDATE': date,
        'AGE_PAR': list(df_age['COUNT(age)'])
    }

    return render(request, 'index.html', context)

def data(request, state):
    conn = sqlite3.connect(settings.DB_PATH)
    col = itemgetter(*settings.INFECTED_LIST_SIMPLE_COLUMN_INDEX)(settings.INFECTED_LIST_COLUMN_NAME)

    df = pd.DataFrame(list(InfectedPerson.objects.filter(state=state).values('state', 'pat_id', 'announce_date', 'infected_date', 'living_city', 'age', 'sex', 'status', 'symptoms', 'occupation', 'close_contact')))

    df.replace([None], '', inplace=True)
    df['pat_id'] = df['pat_id'].apply(lambda x: '<a href="/data/{1}/{0}">{0}</a>'.format(x, state))
    df['sex'] = df['sex'].replace(settings.SEX_DIC)
    df['state'] = df['state'].replace(dict(State.objects.values_list('romam', 'jp')))
    df = df.rename(columns=settings.INFECTED_LIST_HEADER_DICT)
    conn.close()
    table = df.to_html(index=False, escape=False, table_id='data_table', classes='table table-bordered table-striped')
    context = {'INFECTED_LIST': table}

    return render(request, 'data.html', context)

def detail(request, state, id):

    conn = sqlite3.connect(settings.DB_PATH)

    df = pd.DataFrame(list(InfectedPerson.objects.filter(pat_id=id).filter(state=state).values()))

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
    datelist, inf_list = stateutil.getNumByState(conn, 'infected_date', 'state')
    datelist, ann_list = stateutil.getNumByState(conn, 'announce_date', 'state')
    age_label, age_list = stateutil.getNumByAge(conn, 'announce_date', 'age')
    conn.close()

    context = {
        'CHART_LABEL': datelist, 'INFECTED_NUM': inf_list, 'ANNOUNCE_NUM': ann_list,
        'AGE_LABEL': age_label, 'AGE_NUM': age_list,
    }

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

def state(request, state):

    inf_list = []
    ann_list = []
    age_label = []
    age_list = []

    lay = ''

    sname = State.objects.get(romam=state).jp
    state_id = State.objects.get(romam=state).id

    datelist = getDateLabelList()
    inf_numbers = pd.DataFrame(InfectedPerson.objects.filter(state=state).values('infected_date').annotate(dcount=Count('infected_date')))
    ann_numbers = pd.DataFrame(InfectedPerson.objects.filter(state=state).values('announce_date').annotate(dcount=Count('announce_date')))


    if len(inf_numbers.all()) > 0 and len(ann_numbers.all()) > 0:
        lday = max(ann_numbers['announce_date'].dropna().values,
                   key=lambda d: datetime.datetime.strptime(d, '%Y/%m/%d'))
        for d in datelist:
            inf = inf_numbers.query('infected_date in ["%s"]' % (str(d)))['dcount'].tolist()
            inf_list.append( inf[0] if len(inf) > 0 else 0 )

            ann = ann_numbers.query('announce_date in ["%s"]' % (str(d)))['dcount'].tolist()
            ann_list.append( ann[0] if len(ann) > 0 else 0 )

    age_numbers = pd.DataFrame(InfectedPerson.objects.filter(state=state).filter(age__lte=90).values('age', 'announce_date').annotate(age_count=Count('age')).annotate(ann_count=Count('announce_date')))
    color = settings.CHART_COLOR

    if len(age_numbers.all()) > 0:
        for age in np.arange(0, 10):
            dnum = []
            for d in datelist:
                inf_num = age_numbers[age_numbers['announce_date'] == d][age_numbers['age'] == age*10]['ann_count'].values
                if len(inf_num) > 0:
                    dnum.append(inf_num[0])
                else:
                    dnum.append(0)
            age_list.append([age*10, dnum, color[age]])

    numbers = JapanInfectedNumber.objects.filter(state_id=state_id).values_list('positive', 'hospitalization', 'discharge', 'death', 'positive_plus', 'date').order_by('date').reverse()
    numbers_amount = numbers.filter(date=numbers[0][5]).order_by('positive')
    numbers = numbers.reverse()

    city_list = pd.DataFrame(InfectedPerson.objects.filter(state=state).values('living_city').annotate(city_count=Count('living_city'))).dropna()

    context = {
        'CHART_LABEL': datelist, 'INFECTED_NUM': inf_list, 'ANNOUNCE_NUM': ann_list,
        'AGE_LABEL': datelist, 'AGE_NUM': age_list, 'AMOUNT': list(numbers_amount[0]), 'STATE_NAME': sname,
        'CITY_LIST': city_list.values.tolist(), 'SNAME': sname, 'LAST_DAY': lday, 'INF_NUM': numbers,
    }

    return render(request, 'state.html', context)


def cluster(request):

    states = pd.DataFrame(State.objects.values('id', 'romam', 'jp', 'color')).sort_values('id')
    loc_numbers = pd.DataFrame(InfectedPerson.objects.values('cluster_location').annotate(ccount=Count('cluster_location')))
    inf_numbers = pd.DataFrame(InfectedPerson.objects.values('cluster_location', 'state').annotate(ccount=Count('cluster_location')).annotate(ccount=Count('state')))

    loc_numbers = loc_numbers.dropna().sort_values('ccount', ascending=False)
    inf_numbers = inf_numbers.dropna()

    print(loc_numbers.values.tolist())
    print(inf_numbers.values.tolist())
#    print(states)

    data = []
    for st in states.values.tolist():
        st_data = []
        for loc in loc_numbers.values.tolist():
            d = inf_numbers[(inf_numbers['cluster_location'] == loc[0]) & (inf_numbers['state'] == st[1])]
            if len(d) > 0:
                st_data.append(d.values.tolist()[0][2])
            else:
                st_data.append(0)
        data.append([st_data, st[2], st[3]])

    print(data)

    context = {
        'CHART_LABEL': loc_numbers['cluster_location'].values.tolist(),
#        'INFECTED_NUM': inf_numbers['ccount'].values.tolist(),
        'INFECTED_NUM': data,
    }

    return render(request, 'cluster.html', context)
