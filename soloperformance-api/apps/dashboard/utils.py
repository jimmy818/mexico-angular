import calendar
import datetime


def get_dates_range(starts, ends):
    from datetime import timedelta, date
    for n in range(int ((ends - starts).days)+1):
        yield starts + timedelta(n)
        

def get_text_month(year,month):
    return datetime.datetime.strptime('{}-{}-01'.format(year,month), '%Y-%m-%d').strftime("%Y-%m-%d")