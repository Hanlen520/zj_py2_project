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


if __name__ == '__main__':
    
    print os.path.basename(__file__), 'DONE!'
