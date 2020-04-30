

import requests
from coviddb.models import InfectedPerson

from coviddb.util.util import is_int, createDateStr
from io import BytesIO

import pandas
from tika import parser

pandas.set_option('display.max_columns', 500)
pandas.set_option('display.max_rows', 500)
pandas.set_option("display.width", 500)

def getTokyoData(url):

    response = requests.get(url)

    if response.status_code != 200:
        return

    data = []

    tdata = []
    for line in response.text.splitlines():
        tdata.append(line.split(','))

    for row in tdata:
        if is_int(row[0]):
            p = InfectedPerson()
            p.state = 'tokyo'
            p.pat_id = row[0]
            p.city_no = row[1]
            p.living_city = row[3]
            p.announce_date = createDateStr(row[4])
            p.infected_date = createDateStr(row[6])
            p.living_state = '東京都' if row[7] == '都内' else row[7]
            p.setAge(row[8])
            p.setSexStr(row[9])
            p.living_state = row[11]
            p.symptoms = row[12]
            p.travel_history = row[13]
            p.remarks = row[14]
            p.discharge = row[15]

            data.append(p.to_csv())

    return data

def getOsakaData(url):

    response = requests.get(url)

    if response.status_code != 200:
        return

    df = pandas.read_excel(BytesIO(response.content), sheet_name='個票')

    df = df.rename(columns=lambda x: x if not 'Unnamed' in str(x) else '')
    df = df.reset_index()
    df = df.fillna('')

    data = []

    for d in df.iterrows():
        if (type(d[1][1]) == float):
            d[1][1] = int(d[1][1])
        if (type(d[1][1]) == int):
            p = InfectedPerson()
            p.state = 'osaka'
            p.pat_id = int(d[1][1])
            p.age = d[1][2]
            p.setSexStr(d[1][3])
            p.living_city = str(d[1][4])
#            p.living_city = str(d[1][4]) + str(d[1][6])
            p.occupation = job = d[1][6]
            p.infected_date = createDateStr(d[1][7])
            p.status = d[1][8]

            p.setCloseContact(d[1][9])

            p.remarks = d[1][10]

            data.append(p.to_csv())

    return data


def getHokkaidoData(url):

    response = requests.get(url)
    response.encoding = 'Shift-JIS'

    if response.status_code != 200:
        return

    data = []
    tdata = []
    for line in response.text.splitlines():
        tdata.append(line.split(','))


    for row in tdata:
        if is_int(row[0]):
            p = InfectedPerson()
            p.state = 'hokkaido'
            p.pat_id = row[0]
            p.city_no = ''
            p.living_city = row[3]
            p.announce_date = createDateStr(row[1].split('T')[0])
            p.infected_date = ''
            p.setAge(row[12])
            p.setSexStr(row[5])
            p.occupation = row[6]
            p.living_state = '北海道'
            p.symptoms = ''
            p.travel_history = 0
            p.remarks = row[7] + row[11]
            p.death_date = row[8]
            p.setStatus(row[7])

            for c_no in row[10].split('No.'):
                c_no = c_no.replace('No.', '')
                c_no = c_no.replace(' ', '')
                p.setCloseContact(c_no)

            data.append(p.to_csv())

    return data

def getHyogoData(url):

    response = requests.get(url)
    response.encoding = 'Shift-JIS'

    if response.status_code != 200:
        return

    df = pandas.read_excel(response.content)
    df = df.rename(columns=lambda x: x if not 'Unnamed' in str(x) else '')
    df = df.reset_index()

    data = []

    for d in df.iterrows():
        if is_int(d[1][2]):
            p = InfectedPerson()
            p.state = 'hyogo'
            p.living_state = '兵庫県'
            p.pat_id = d[1][2]
            p.city_no = ''
            p.announce_date = createDateStr(d[1][3])
            p.setAge(str(d[1][4]))
            p.setSexStr(d[1][5])
            p.living_city = d[1][7]
            p.occupation = d[1][8]
            p.infected_date = createDateStr(d[1][9])
            if d[1][10] == 'なし':
                p.travel_history = 0
            elif d[1][10] == 'あり':
                p.travel_history = 1
            p.remarks = d[1][11]
            if d[1][12] == '○':
                p.cluster_name = '認定こども園'
            elif d[1][13] == '○':
                p.cluster_name = '北播磨総合医療センター'
            elif d[1][14] == '○':
                p.cluster_name = '宝塚第一病院'
            elif d[1][15] == '○':
                p.cluster_name = '仁恵病院'
            elif d[1][16] == '○':
                p.cluster_name = '神戸市中央市民病院'
            elif d[1][17] == '○':
                p.cluster_name = 'グリーンアルス関係'
            elif d[1][18] == '○':
                p.cluster_name = '介護保険通所事業所'
            elif d[1][19] == '○':
                p.cluster_name = 'ライブ関係'

            data.insert(0, p.to_csv())

    return data

def getChibaData(url):

    response = requests.get(url)

    if response.status_code != 200:
        return

    file_data = parser.from_buffer(response.content)
    text = file_data["content"]

    data = []
