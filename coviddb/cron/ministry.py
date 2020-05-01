
import django
import os
import requests
import pandas
from datetime import datetime, timedelta
from django.conf import settings
from tika import parser
from bs4 import BeautifulSoup
import traceback

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "coviddb.settings")
django.setup()

from coviddb.models import State, JapanInfectedNumber
from coviddb.util.util import *
from coviddb.util.mailutil import send
from coviddb.util.util import trans_fullwidth

def run():
    try:
        day_delta = 0
        pdf_url = getURL(day_delta)
        if(len(pdf_url) <= 0):
            failMail("No URL.")
        else:
            getData(pdf_url, day_delta)

    except Exception as e:
        failMail(str(traceback.format_exc()))
        traceback.print_exc()

def failMail(msg):
    send(settings.AUDIT_ADDR, settings.AUDIT_ADDR, "COVID-19 Japan Database", msg)

def getData(url, day_delta):
    word_delta = 0
    data = getKouseiData(url, word_delta)
    df = pandas.DataFrame(data).fillna(0)

    for data in df.iterrows():
        regist(list(data[1]), day_delta)

    send(settings.AUDIT_ADDR, settings.AUDIT_ADDR, "COVID-19 Japan Database", "データ取り込み成功" + str(data))

def regist(d, day_delta):
    st = State.objects.get(jp=d[0])
    d[1] = d[1] if is_int(d[1]) else 0
    d[2] = d[2] if is_int(d[2]) else 0
    d[3] = d[3] if is_float(d[3]) else 0
    d[4] = d[4] if is_int(d[4]) else 0
    d[5] = d[5] if is_float(d[5]) else 0
    d[6] = d[6] if is_int(d[6]) else 0
    d[7] = d[7] if is_float(d[7]) else 0
    d[8] = d[8] if is_int(d[8]) else 0
    d[9] = d[9] if is_float(d[9]) else 0

    JapanInfectedNumber.objects.update_or_create(
        state_id=st.id,
        date=(datetime.date.today() - datetime.timedelta(days=2+day_delta)).strftime('%Y/%m/%d'),
        defaults={
            'state': st.jp,
            'positive': d[1],
            'positive_plus': d[2],
            'positive_per': d[3],
            'hospitalization': d[4],
            'hospitalization_per': d[5],
            'discharge': d[6],
            'discharge_per': d[7],
            'death': d[8],
            'death_per': d[9],
        }
    )

def getURL(day_delta):
    d_today = datetime.datetime.today() - timedelta(days=1+day_delta)
    mon_str = datetime.datetime.strftime(d_today, '%Y%m')
    url = 'https://www.mhlw.go.jp/stf/houdou/houdou_list_%s.html' % mon_str

    res = requests.get(url)
    content_type_encoding = res.encoding if res.encoding != 'ISO-8859-1' else None
    soup = BeautifulSoup(res.content, 'html.parser', from_encoding=content_type_encoding)

    links = soup.find_all('a')

    for l in links:
        if "新型コロナウイルス感染症の現在の状況" in l.get_text():
            start = l.get_text().find("令和")
            end = l.get_text().rfind("版")

            date_str = trans_fullwidth(l.get_text()[start:end])
            date_str = date_str.replace("令和", "").replace("年", "/").replace("月", "/").replace("日", "")

            ymd = date_str.split('/')
            ymd = list(map(lambda x: int(x), ymd))
            ymd[0] = int(ymd[0]) + 2018

            if datetime.datetime.strftime(d_today, '%Y%m%d') == "%04d%02d%02d" % (ymd[0], ymd[1], ymd[2]):
                date_url = "https://www.mhlw.go.jp" + l.get('href')

                sub_res = requests.get(date_url)
                sub_soup = BeautifulSoup(sub_res.content, 'html.parser', from_encoding=content_type_encoding)
                for ln in sub_soup.find_all('a'):
                    if "における都道府県別" in ln.get_text():
                        return "https://www.mhlw.go.jp" + ln.get('href')

    return ""

def getKouseiData(url, word_delta):
    response = requests.get(url)

    if response.status_code != 200:
        return

    data = []

    file_data = parser.from_buffer(response.content)
    # file_data = parser.from_file("./temp.pdf")
    text = file_data["content"]

    for line in text.splitlines():
        words = line.split(' ')
        if (len(words) >= 6):
            if words[0+word_delta].endswith('都') or words[0+word_delta].endswith('道') or words[0+word_delta].endswith('府') or words[0+word_delta].endswith('県'):
                words[0+word_delta].replace(' ', '')
                for i in range(len(words)):
                    words[i] = words[i].replace('%', '')
                    words[i] = words[i].replace('※', '')
                data.append(words)


    return data;

run()

