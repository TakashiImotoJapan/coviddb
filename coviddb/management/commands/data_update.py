
import pandas as pd
from coviddb.models import InfectedPerson, State
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    def handle(self, *args, **options):

        all = pd.DataFrame(InfectedPerson.objects.all().values_list('state', 'announce_date'))

        all.columns = ['state', 'announce_date']
        all = all.sort_values('announce_date', ascending=False)

        states_name = all.groupby('state')['state'].apply(list)
        states_date = all.groupby('state')['announce_date'].apply(list)

        json_data = pd.DataFrame(columns = ['id', 'state_name', 'last_update'])

        df_list = []

        for names, dates in zip(states_name, states_date):
            state = State.objects.get(romam=names[0])

            json_data = json_data.append(pd.Series([state.id, state.jp, dates[0]], index=json_data.columns, name=names[0]))

        out = json_data.to_json(orient='records')

        with open('coviddb/json/data_update.json', 'w') as f:
            f.write(out)
