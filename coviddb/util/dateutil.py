
from datetime import datetime as dt
from datetime import timedelta

def getDateLabelList():

    start = dt.strptime("2020/01/15", '%Y/%m/%d')  # 開始日
    end = dt.now()

    datelist = list(map(lambda x, y=start: (y + timedelta(days=x)).strftime("%Y/%m/%d"), range((end - start).days + 1)))

    return datelist

