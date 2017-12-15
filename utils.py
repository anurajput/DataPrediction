from collections import defaultdict
from sqlalchemy.inspection import inspect


from random import randint
import time


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

def smart_int(s):
    try:
        return int(s)
    except:
        return 0


if __name__ == "__main__":
    print get_date_from_filename("abc20171213")
