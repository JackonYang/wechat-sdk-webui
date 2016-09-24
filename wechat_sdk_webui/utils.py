# -*- coding:utf-8 -*-
import random
import time


def get_timestamp():
    # millisecond required
    return int(time.time() * 1000)


def gen_device_id(length=15):
    return 'e%s' % random.randint(10 ** length, 10 ** (length + 1) - 1)


if __name__ == '__main__':
    print get_timestamp()
    print gen_device_id()
