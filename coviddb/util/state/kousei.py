

import requests
import datetime
from tika import parser
from coviddb.models import JapanInfectedNumber, State

from django.core.management.base import BaseCommand

def getKouseiData(url):
    response = requests.get(url)

    if response.status_code != 200:
        return

    data = []

    file_data = parser.from_buffer(response.content)
    # file_data = parser.from_file("./temp.pdf")
    text = file_data["content"]
    for line in text.splitlines():
        words = line.split(' ')
        if words[0].endswith('都') or words[0].endswith('道') or words[0].endswith('府') or words[0].endswith('県'):
            if (len(words) >= 6):
                words[0].replace(' ', '')
                for i in range(len(words)):
                    words[i] = words[i].replace('%', '')
                    words[i] = words[i].replace('※', '')
                data.append(words)

    return data;
