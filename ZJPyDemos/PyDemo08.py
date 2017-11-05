# -*- coding: utf-8 -*-
'''
Created on 2017-5-27

@author: zhengjin
'''

import os

from PyDemo01 import run_ex_by_flag

# EXAMPLE 01, Tips
def ex0101():
    my_map = {'k1':'v1', 'k2':'v2', 'k3':'v3'}
    print 'Yes:'
    for k in my_map:
        print 'key:', k

    print 'No:'
    for k in my_map.keys():
        print 'key:', k
run_ex_by_flag(ex0101)

def ex0102():
    def condition_exp_test(cond):
        return 'Yes' if cond else 'No'
    print 'results:', condition_exp_test(False)
run_ex_by_flag(ex0102)

def ex0103():
    # write long string in multiple lines
    my_str = ('this is test1, '
              'this is test2, '
              'this is test3, ' 'this is test4')
    print 'output:', my_str
run_ex_by_flag(ex0103)


# EXAMPLE 02, get prime number
def ex02():
    num = 30
    tmp_lst = []
    for i in xrange(3, num):
        for j in xrange(2, i):
            if i % j == 0:
                break
        else:
            tmp_lst.append(i)
    print tmp_lst

run_ex_by_flag(ex02)


# EXAMPLE 03, classmethod and staticmethod
def ex03():
    class TestSuper(object):
        @staticmethod
        def getMessage():
            return 'in super:'
        @classmethod
        def printMessage(cls):
            print cls.getMessage(), cls.__name__
    
    class TestSub(TestSuper):
        @staticmethod
        def getMessage():
            return 'in sub:'

    TestSuper.printMessage()
    TestSub.printMessage()

run_ex_by_flag(ex03)


# EXAMPLE 04, ThreadPoolExecutor
def ex04():
    from concurrent.futures import ThreadPoolExecutor
    import time

    def _return_future_result(msg):
        time.sleep(2)
        return msg

    pool = ThreadPoolExecutor(max_workers=2)
    future1 = pool.submit(_return_future_result, ('hello'))
    future2 = pool.submit(_return_future_result, ('world'))
    
    print future1.done()
    time.sleep(3)  # wait in main thread
    print future2.done()

    print future1.result()
    print future2.result()

run_ex_by_flag(ex04)


# EXAMPLE 05, ThreadPoolExecutor, wait()
def ex05():
    from concurrent.futures import ThreadPoolExecutor, wait
    from time import sleep
    from random import randint
    
    def _return_after_random_secs(num):
        sleep(randint(1, 5))
        return 'Return of %d' % num
    
    pool = ThreadPoolExecutor(max_workers=2)
    futures = []
    for x in xrange(5):
        futures.append(pool.submit(_return_after_random_secs, x))
    results = wait(futures)  # default ALL_COMPLETED
#     results = wait(futures, timeout=None, return_when='FIRST_COMPLETED')
    print results
    for res in results.done:
        print res.result()

run_ex_by_flag(ex05)


# EXAMPLE 0601, ThreadPoolExecutor, as_completed()
def ex0601():
    from concurrent.futures import ThreadPoolExecutor, as_completed
    from time import sleep
    from random import randint
    
    nums = (1, 2, 3, 4, 5)
    def _return_after_random_secs(num):
        sleep(randint(1, 5))
        return 'Return of %d' % num

    # as_completed() returns a generator that yields completed future each time, print in random sequence
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_num = {executor.submit(_return_after_random_secs, num):num for num in nums}
        # as_completed() returns: an iterator that yields the given Futures as they complete
        for future in as_completed(future_to_num):
            num = future_to_num[future]
            try:
                data = future.result()
            except Exception as ex:
                print 'number %d generated an exception: %s' % (num, ex)
            else:
                print 'results for %d: %s' % (num, data)

run_ex_by_flag(ex0601)


# EXAMPLE 0602, ThreadPoolExecutor, map()
def ex0602():
    from concurrent.futures import ThreadPoolExecutor
    from time import sleep
    from random import randint

    nums = (1, 2, 3, 4, 5)
    def _return_after_random_secs(num):
        sleep(randint(1, 5))
        return 'Return of %d' % num

    # map(), wait all completed and return once, print as sequence in nums
    with ThreadPoolExecutor(max_workers=5) as executor:
        for num, data in zip(nums, executor.map(_return_after_random_secs, nums)):
            print 'results for %d: %s' % (num, data)

run_ex_by_flag(ex0602)


if __name__ == '__main__':
    
    print os.path.basename(__file__), 'DONE!'
