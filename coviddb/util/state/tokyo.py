

import requests
from coviddb.models import InfectedPerson

from coviddb.util.util import is_int

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
            p.announce_date = p.createDateStr(row[4])
            p.infected_date = p.createDateStr(row[6])
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
