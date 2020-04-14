import pandas as pd

from django.template.response import TemplateResponse
from django.urls import path
from coviddb.util.state.kousei import getKouseiData
from coviddb.util.state.state import *

from .models import State, JapanInfectedNumber
from django.contrib import admin
from coviddb.util.util import is_float, is_int
import datetime

admin.site.register(State)


@admin.register(JapanInfectedNumber)
class MyModelAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()

        my_urls = [
            path('kousei/', self.admin_site.admin_view(self.kousei, cacheable=True)),
            path('tokyo/', self.admin_site.admin_view(self.state, cacheable=True)),
            path('osaka/', self.admin_site.admin_view(self.state, cacheable=True)),
            path('hokkaido/', self.admin_site.admin_view(self.state, cacheable=True)),
            path('hyogo/', self.admin_site.admin_view(self.state, cacheable=True)),
            path('chiba/', self.admin_site.admin_view(self.state, cacheable=True)),
        ]
        return my_urls + urls

    def kousei(self, request, *args, **kwargs):

        list_data = []
        table = ''

        if request.POST.get('url', None):
            print(request.POST.get('url', None))
            data = getKouseiData(request.POST.get('url', None))
            if data != None and len(data) > 0:
                list_data = pd.DataFrame(data).to_csv(header=False, index=False)
                table = pd.DataFrame(data).to_html()

        if request.POST.get('data', None):
            data = request.POST.get('data', None)

            if(len(data) > 100):

                regist = []
                for line in data.splitlines():
                    regist.append(line.split(','))
                print(regist)
                for d in regist:
                    print(d)
                    st = State.objects.get(jp=d[0])
                    d[1] = d[1] if is_int(d[1]) else 0
                    d[2] = d[2] if is_int(d[2]) else 0
                    d[3] = d[3] if is_float(d[3]) else 0
                    d[4] = d[4] if is_int(d[4]) else 0
                    d[6] = d[6] if is_int(d[6]) else 0
                    d[8] = d[8] if is_int(d[8]) else 0

                    JapanInfectedNumber.objects.update_or_create(
                        state_id = st.id,
                        defaults={
                            'state': st.jp,
                            'date': datetime.date.today().strftime('%Y/%m/%d'),
                            'positive': d[1],
                            'plus': d[2],
                            'discharge_per': d[3],
                            'hospitalization': d[4],
                            'discharge': d[6],
                            'death': d[8],
                        }
                    )

        context = {'LIST_DATA': list_data, 'TABLE_DATA': table}

        return TemplateResponse(request, "admin/kousei.html", context)

    def state(self, request, *args, **kwargs):

        csv_data = ''

        if request.POST.get('url', None):
            request_url = (str(request.path).split('/'))
            state = request_url[len(request_url)-2]
            if state == 'tokyo':
                csv_data = getTokyoData(request.POST.get('url', None))
            elif state == 'hokkaido':
                csv_data = getHokkaidoData(request.POST.get('url', None))
            elif state == 'osaka':
                csv_data = getOsakaData(request.POST.get('url', None))
            elif state == 'hyogo':
                csv_data = getHyogoData(request.POST.get('url', None))
            elif state == 'chiba':
                csv_data = getChibaData(request.POST.get('url', None))

        context = {'URL': request.path, 'CSV_DATA': csv_data}

        return TemplateResponse(request, "admin/view_csv.html", context)

