from random import randint
import time


SLEEP_MIN = 1  # in seconds
SLEEP_MAX = 5  # in seconds


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
