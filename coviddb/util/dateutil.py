
from datetime import datetime as dt
from datetime import timedelta

def getDateLabelList(start="2020/01/15", end=""):

    start_dt = dt.strptime(start, '%Y/%m/%d')

    if len(end) > 0:
        end_dt = dt.strptime(end, '%Y/%m/%d')
    else:
        end_dt = dt.now()

    datelist = list(map(lambda x, y=start_dt: (y + timedelta(days=x)).strftime("%Y/%m/%d"), range((end_dt - start_dt).days - 1)))

    return datelist

