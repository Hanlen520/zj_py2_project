# -*- coding: utf-8 -*-
'''
Created on 2017-5-27

@author: zhengjin
'''
import os

from PyDemo01 import run_ex_by_flag

# collections
# EXAMPLE 01, defaultdict
def ex01_01():
    from collections import defaultdict
    
    tmp_lst = [('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 1)]
    d_dict = defaultdict(list)  # set default value to []
    for k, v in tmp_lst:
        d_dict[k].append(v)

    print sorted(d_dict.iteritems())
run_ex_by_flag(ex01_01)

def ex01_02():
    tmp_lst = [('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 1)]
    d_dict = {}
    for k, v in tmp_lst:
        d_dict.setdefault(k, []).append(v)  # set default value to []

    print sorted(d_dict.items())
run_ex_by_flag(ex01_02)

def ex01_03():
    from collections import defaultdict
    
    tmp_lst = [('red', 1), ('blue', 2), ('red', 3), ('blue', 4), ('red', 1), ('blue', 4)]
    d_dict = defaultdict(set)  # set default value to set (include distinct value)
    for k, v in tmp_lst:
        d_dict[k].add(v)

    print sorted(d_dict.items())
run_ex_by_flag(ex01_03)


# EXAMPLE 02, OrderedDict
def ex02():
    from collections import OrderedDict
    
    tmp_dict = {'banana': 3, 'apple': 4, 'pear': 1, 'orange': 2}
    print OrderedDict(sorted(tmp_dict.items(), key=lambda t:t[0]))
    print OrderedDict(sorted(tmp_dict.iteritems(), key=lambda t:len(t[0])))

    tmp_or_dict = OrderedDict.fromkeys('abcde', 'null')
    print tmp_or_dict

run_ex_by_flag(ex02)


# EXAMPLE 03, deque
def ex03():
    from collections import deque
    
    tmp_deque = deque(range(10), maxlen=10)
    print tmp_deque

    tmp_deque.appendleft(-1)
    print tmp_deque

    tmp_deque.extendleft([10, 20, 30])
    print tmp_deque
    
run_ex_by_flag(ex03)


# EXAMPLE 04, Counter
def ex04():
    from collections import Counter

    tmp_ct = Counter('abracadabra')
    print tmp_ct
    
    tmp_ct = Counter({'a': 5, 'r': 2, 'b': 2, 'd': 1, 'c': 1})
    tmp_ct.update('aaaaazzz')
    print tmp_ct
    print tmp_ct.most_common(2)
    print tmp_ct.elements()
    print ''.join(tmp_ct.elements())

run_ex_by_flag(ex04)

# EXAMPLE 05, namedtuple
def ex05():
    from collections import namedtuple
    
    City = namedtuple('City', 'name country population coordinates')
    tokyo = City('Tokyo', 'JP', 36.933, (35.689722, 139.691667))
    
    print City._fields
    print tokyo
    print tokyo.population
    print tokyo.coordinates
    print tokyo[1]

run_ex_by_flag(ex05)


if __name__ == '__main__':

    print '%s done!' % os.path.basename(__file__)
