

import requests
from tika import parser
import django
import os

def getKouseiData(url, delta):
    response = requests.get(url)

    if response.status_code != 200:
        return

    data = []

    file_data = parser.from_buffer(response.content)
    # file_data = parser.from_file("./temp.pdf")
    text = file_data["content"]

    print(text)

    for line in text.splitlines():
        words = line.split(' ')
        if (len(words) >= 6):
            if words[0+delta].endswith('都') or words[0+delta].endswith('道') or words[0+delta].endswith('府') or words[0+delta].endswith('県'):
                words[0+delta].replace(' ', '')
                for i in range(len(words)):
                    words[i] = words[i].replace('%', '')
                    words[i] = words[i].replace('※', '')
                data.append(words)


    return data;
