
import pandas
import glob
import django
import os
import datetime
import pandas

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "coviddb.settings")
django.setup()

flist = glob.glob("../../data/state/*.xlsx")

pandas.set_option('display.max_columns', 500)
pandas.set_option('display.max_rows', 500)
pandas.set_option("display.width", 500)

from coviddb.models import InfectedPerson

all = pandas.DataFrame(InfectedPerson.objects.all())

print(all)