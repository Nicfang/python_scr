#!/usr/bin/env python
# -*- coding: utf-8 -*-

from multiprocessing import Process
import time


def task(msg):
    print 'hello, %s' % msg
    time.sleep(1)


if __name__ == '__main__':

    table_list = ['world','tom','pit','nic']
    for i in range(4):
        p = Process(target=task, args=(i,))
        p.start()
        # table_list.remove(i)



