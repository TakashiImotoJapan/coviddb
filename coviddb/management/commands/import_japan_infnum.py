
import requests
import datetime
from tika import parser
from coviddb.models import JapanInfectedNumber, State

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):

        response = requests.get("https://www.mhlw.go.jp/content/10900000/000620956.pdf")

        data = []

        file_data = parser.from_buffer(response.content)
        # file_data = parser.from_file("./temp.pdf")
        text = file_data["content"]
        for line in text.splitlines():
            words = line.split(' ')
            if words[0].endswith('都') or words[0].endswith('道') or words[0].endswith('府') or words[0].endswith('県'):
                if(len(words) == 11):
                    words[0].replace(' ', '')
                    data.append(words)

        JapanInfectedNumber.objects.all().delete()

        for d in data:
            st = State.objects.get(jp=d[0])
            JapanInfectedNumber.objects.update_or_create(
                state_id = st.id,
                state = st.jp,
                date = datetime.date.today().strftime('%Y/%m/%d'),
                positive = d[2],
                plus = d[3],
                discharge_per = d[4],
                hospitalization = d[5],
                discharge = d[7],
                death = d[9],
            )
