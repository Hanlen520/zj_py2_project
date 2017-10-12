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


if __name__ == '__main__':
    
    print os.path.basename(__file__), 'DONE!'
