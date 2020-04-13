

import requests
from coviddb.models import InfectedPerson

from coviddb.util.util import is_int

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
            p.announce_date = p.createDateStr(row[1].split('T')[0])
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
