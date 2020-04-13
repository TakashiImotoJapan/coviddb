
import datetime

def createDateStr(val):
    print(type(val))
    if type(val) == datetime.datetime:
        return val.strftime('%Y/%m/%d')
    elif type(val) == int:
        print(val)
        return datetime.datetime(1899, 12, 30) + datetime.timedelta(days=val)
    elif type(val) == str:
        val = val.replace('-', '/')
        val = val.replace('月', '/')
        val = val.replace('日',  '/')
        return val
    else:
        return ''

def is_float(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return True

def is_int(n):
    try:
        int(n)
    except ValueError:
        return False
    else:
        return True