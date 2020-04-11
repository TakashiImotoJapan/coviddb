
import requests
import datetime
from tika import parser
from coviddb.models import JapanInfectedNumber, State

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):

        response = requests.get("https://www.mhlw.go.jp/content/10906000/000621070.pdf")

        if response.status_code != 200:
            return

        data = []

        file_data = parser.from_buffer(response.content)
        # file_data = parser.from_file("./temp.pdf")
        text = file_data["content"]
        for line in text.splitlines():
            words = line.split(' ')
            if words[0].endswith('都') or words[0].endswith('道') or words[0].endswith('府') or words[0].endswith('県'):
                if(len(words) >= 6):
                    words[0].replace(' ', '')
                    data.append(words)

#        print(data)
        if(len(data) < 40):
            return

        for d in data:
            st = State.objects.get(jp=d[0])
            JapanInfectedNumber.objects.update_or_create(
                state_id = st.id,
                state = st.jp,
                date = datetime.date.today().strftime('%Y/%m/%d'),
                positive = d[1],
                plus = d[2],
                discharge_per = d[3],
                hospitalization = d[4],
                discharge = d[6],
                death = d[8],
            )
