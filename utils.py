from collections import defaultdict
from sqlalchemy.inspection import inspect


from random import randint
import time
from datetime import datetime
from datetime import timedelta


SLEEP_MIN = 1  # in seconds
SLEEP_MAX = 5  # in seconds


def query_to_list(rset):
    """List of result
    Return: columns name, list of result
    """
    result = []
    for obj in rset:
        instance = inspect(obj)
        items = instance.attrs.items()
        result.append([x.value for _,x in items])
    return instance.attrs.keys(), result


def query_to_dict(rset):
    result = defaultdict(list)
    for obj in rset:
        instance = inspect(obj)
        for key, x in instance.attrs.items():
            result[key].append(x.value)
    return result


def get_rand_in_range(min, max):
    return randint(min, max)


def get_sleep():
    return get_rand_in_range(SLEEP_MIN, SLEEP_MAX)


def sleep_timer(file_name):
    val = get_sleep()
    print("\n\n[%s] :: SLEEPING FOR %d seconds.....\n\n" % (file_name, val))
    time.sleep(val)
    print("\n\n[%s] :: RESUMED \n\n" % file_name)


def log(tag, method_name, msg):
        print('[%s] :: %s :: %s' % (tag, method_name, msg))


def get_date_from_filename(csv):
    sub = csv.split('.')
    x = sub[0]
    date = x[-8:]
    year = date[:4]
    month = date[4:-2]
    day = date[-2:]
    return "%s-%s-%s" % (year, month, day)


def date_str(date):
    if not len(date) == 8:
        print "[WARNING] :: date_str() got invalid date:", date
        return date
    year = date[:4]
    month = date[4:-2]
    month_date = date[-2:]
    return '%s-%s-%s' % (year, month, month_date)


def smart_int(s):
    try:
        return int(s)
    except:
        return 0

def days_left_for_next_produce(next_produce_date, date, supply_for_days):
    try:
        if next_produce_date == "0":
            return supply_for_days
        date_format = '%Y-%m-%d'
        s = datetime.strptime(date, date_format)  
        e = datetime.strptime(next_produce_date, date_format)  
        delta = e - s
        return delta.days
    except Exception as exp:
        print "[WARNING] :: days_left_for_next_produce(%s -> %s) got exception: %s" % (next_produce_date, date, exp)
        return supply_for_days

def runs_out_before_next_stock(next_produce_date, date, supply_for_days):
    try:
        if next_produce_date == "0":
            return 0
        date_format = '%Y-%m-%d'
        s = datetime.strptime(date, date_format)  
        e = datetime.strptime(next_produce_date, date_format)  
        no_of_days_left = e - s

        if no_of_days_left.days > supply_for_days:
            return 1
        else:
            return 0
    except Exception as exp:
        print "[WARNING] ::  runs_out_before_next_stock () got exception: %s" % exp
        return 0

def date_from_str(s):
    date_format = '%Y-%m-%d'
    return datetime.strptime(s, date_format)  

def inc_day(d):
    return d + timedelta(days=1)


if __name__ == "__main__":
    #print "Date from filename is:", get_date_from_filename("20171213")
    #print "Date str:", date_str("20171213")
    #print "Days delta:", days_delta('2017-12-11', '2017-12-20')
    d = date_from_str("2017-12-13")
    nd = inc_day(d)
    print "Next day:", nd.date()
