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


# EXAMPLE 07, Hackers
def ex0701():
    import time

    # Default parameter values are evaluated when the function definition is executed.
    # same value
    def _print_time_01(when=time.time()):
        return when
    print _print_time_01()
    time.sleep(1)
    print _print_time_01()

    # different value
    def _print_time_02(when=None):
        if when is None:
            when = time.time()
        return when
    print _print_time_02()
    time.sleep(2)
    print _print_time_02()

run_ex_by_flag(ex0701)


def ex0702():
    tmp_object_01 = (1)
    print type(tmp_object_01)

    # define tuple with one element
    tmp_object_02 = (1,)
    print type(tmp_object_02)

run_ex_by_flag(ex0702)


def ex0703():
    def _modify_lst(lst):
        for idx, elem in enumerate(lst):
            if elem % 3 == 0:
                print 'delete element at:', idx
                del lst[idx]
    
    # update list (remove element) when iterator, element move forward
    tmpLst01 = [1, 2, 3, 5, 4, 6]
    _modify_lst(tmpLst01)
    print tmpLst01
    
    # bad
    tmpLst02 = [1, 2, 3, 6, 5, 4]
    _modify_lst(tmpLst02)
    print tmpLst02
    
    # ok, list comprehension
    tmpLst03 = [1, 2, 3, 6, 5, 4]
    print [elem for elem in tmpLst03 if elem % 3 != 0]

run_ex_by_flag(ex0703)


def ex0704():
    # closure
    def _create_multipliers_01():
        return [lambda base: base * i for i in xrange(5)]
    print 'iterator 01:'
    for fn_multiplier in _create_multipliers_01():
        print fn_multiplier(2)

    def _create_multipliers_02():
        return [lambda base, val = i: base * val for i in xrange(5)]
    print 'iterator 02:'
    for fn_multiplier in _create_multipliers_02():
        print fn_multiplier(2)
        
    def _fn_multiplier(value, base=2):
        return base * value
    print 'results:', _fn_multiplier(base=3, value=5)
    print 'results:', _fn_multiplier(value=6)

run_ex_by_flag(ex0704)


def ex0705():
    import sys
    sys.path.append(os.getcwd())
    print sys.path
    
    def _test_import_01():
        import IteratorDemo
        print id(IteratorDemo)
    _test_import_01()

    def _test_import_02():
        import IteratorDemo as module
        print id(module)
    _test_import_02()

    # get different id value as above "imports", so they are different module objects
    def _test_import_03():
        from ZJPyDemos import IteratorDemo
        print id(IteratorDemo)
    _test_import_03()

run_ex_by_flag(ex0705)


# EXAMPLE 08, generate dict
def ex08():
    d = dict(((1, 'one'), (2, 'two'), (3, 'three')))
    print 'dict:', d
    
    names = ['jim', 'tom', 'henry', 'tid']
    
    def _say_hello(name):
        return 'hello ' + name

    name_to_msg1 = dict((name, _say_hello(name)) for name in names)
    print 'type:', type(name_to_msg1)
    print 'value:', name_to_msg1
    
    name_to_msg2 = {name: _say_hello(name) for name in names}
    print 'type:', type(name_to_msg2)
    print 'value:', name_to_msg2

run_ex_by_flag(ex08)


# EXAMPLE 09, global
a = 1
def ex09():
    def _test_print1():
        global a
        a += 1
        print 'value:', a

    def _test_print2():
        ret = a + 1
        print 'return value:', ret

    _test_print1()
    _test_print2()

run_ex_by_flag(ex09)


# EXAMPLE 10, itertools
def ex1001():
    # map, starmap
    lst = map(lambda x: x * 2, [1, 2, 3, 4, 5])
    print type(lst)
    print 'value:', lst

    from itertools import starmap
    it = starmap(os.path.join,
            [('/bin', 'python'), ('/usr', 'bin', 'java'),
             ('/usr', 'bin', 'perl'), ('/usr', 'bin', 'ruby')])
    print type(it)
    print 'value:', list(it)

run_ex_by_flag(ex1001)


def ex1002():
    # 1, chain
    from itertools import chain
    lst = [1, 2, 3] + ['a', 'b', 'c']
    print type(lst)
    print 'value:', lst
    
    print 'chain list:', list(chain([1, 2, 3], ['a', 'b', 'c']))
    
    # 2, zip_longest
    r1 = range(2)
    r2 = range(3)
    print 'zip as list:', list(zip(r1, r2))
#     from itertools import zip_longest
    print 'zip as dict:', dict(zip(r1, r2))

run_ex_by_flag(ex1002)


# EXAMPLE 11, operator
def ex11():
    class Student(object):
        def __init__(self, name, grade, age):
            self.name = name
            self.grade = grade
            self.age = age
            
        def __repr__(self):
            return repr((self.name, self.grade, self.age))
#             return 'name: %s grade: %s age: %d' % (self.name, self.grade, self.age)

    from operator import attrgetter, itemgetter
    student_objects = [Student('john', 'A', 15), Student('jane', 'B', 12), Student('dave', 'B', 10), ]
    print 'sorted by lambda:', sorted(student_objects, key=lambda s:s.age)
    print 'sorted by attrgetter:', sorted(student_objects, key=attrgetter('grade', 'age'))
    
    student_tuples = [('john', 'A', 15), ('jane', 'B', 12), ('dave', 'B', 10), ]
    print 'sorted by lambda:', sorted(student_tuples, key=lambda s:s[2])
    print 'sorted by itemgetter:', sorted(student_tuples, key=itemgetter(1, 2))

run_ex_by_flag(ex11)


# EXAMPLE 12, collections
def ex1201():
    # 1. defaultdict
    from collections import defaultdict
    
    s = [('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 1)]
    d1 = defaultdict(list)
    for k, v in s:
        d1[k].append(v)
    print sorted(d1.iteritems())
    
    # 2
    d2 = {}
    for k, v in s:
        d2.setdefault(k, []).append(v)
    print sorted(d2.iteritems())

run_ex_by_flag(ex1201)


def ex1202():
    # OrderedDict
    from collections import OrderedDict
    from operator import itemgetter
    d = {'banana': 3, 'apple': 4, 'pear': 1, 'orange': 2}
    order = OrderedDict(sorted(d.iteritems(), key=itemgetter(1)))
    print order
    print order.popitem(last=True)
    print 'after update:', order

run_ex_by_flag(ex1202)


def ex1203():
    # deque
    from collections import deque
    q = deque(range(10), maxlen=10)
    print q
    q.appendleft(-1)
    print 'after append:', q
    q.extend([10, 11, 12, ])
    print 'after extend:', q

run_ex_by_flag(ex1203)


def ex1204():
    # Counter
    from collections import Counter
    c = Counter('abracadabra')
    print c
    c.update('aaaaazzz')
    print 'after update:', c
    print c.most_common(2)

run_ex_by_flag(ex1204)


# EXAMPLE 13, custom dict
def ex13():
    d1 = dict([('one', 1), ('two', 2), ('three', 3), ])
    print d1
    print 'element:', d1['one']
    
    class MyDict(dict):
        """
        A MyDict object is like a dictionary except "obj.foo" can be used in addition to "obj['foo']".
        """
        def __getattr__(self, key):
            try:
                return self[key]
            except KeyError as k:
                raise AttributeError(k)

        def __setattr__(self, key, value):
            self[key] = value

        def __delattr__(self, key):
            try:
                del self[key]
            except KeyError as k:
                raise AttributeError(k)

        def __repr__(self):
            return '<MyDict %s>' % dict.__repr__(self)
    
    d2 = MyDict([('one', 1), ('two', 2), ('three', 3), ])
    print 'access by index:', d2['two']
    print 'access by attr:', d2.two
    
    del d2.two
    print d2

run_ex_by_flag(ex13)


if __name__ == '__main__':

    print os.path.basename(__file__), 'DONE!'
