# -*- coding: utf-8 -*-
'''
Created on 2017-2-6

@author: zhengjin
'''

from __future__ import division
import os

from PyDemo01 import run_ex_by_flag

# EXAMPLE 01, functional program
def ex01():
    cats = {'Mojo':84, 'Mao-Mao':34, 'Waffles':4, 'Pickles':6}
    for k in cats:
        print k

    print '*' * 20, 'case 1'     
    kittens = []
    for k, v in cats.iteritems():
        if v < 7:
            kittens.append(k)
    print kittens
    del kittens[:]
    
    print '*' * 20, 'case 2'
    kittens = [k for k, v in cats.items() if v < 7]
    print kittens
    del kittens[:]
    
    print '*' * 20, 'case 3'
    kittens = map(lambda (k, v): k, filter(lambda (k, v):v < 7, cats.iteritems()))
    print kittens

run_ex_by_flag(ex01)


# EXAMPLE 02, file read
def ex02():
    tmp_file_path = os.path.join(os.getcwd(), 'zjunittest.log')

    with open(tmp_file_path, 'r') as f:
        print 'type:', type(f)
        if '__enter__' in dir(f) and '__exit__' in dir(f):
            print 'with block'
        if '__iter__' in dir(f):
            print 'iterator'

        for line in f:
            print line.strip()

run_ex_by_flag(ex02)


# EXAMPLE 03, multiple lines
def ex03():
    print 'this is first line.\n' \
           'this is 2nd line.\n'
     
    print ('this is first line.\n'
           'this is 2nd line.\n')

    print '''this is first line.
this is 2nd line.
    '''

run_ex_by_flag(ex03)


# EXAMPLE 04, zip, enumerate
def ex04():
    # zip
    lst_1 = ('k1', 'k2', 'k3')
    lst_2 = ('a', 'b', 'c')
    tmp_ret = zip(lst_1, lst_2)
    print tmp_ret
     
    tmp_d = dict(tmp_ret)
    print tmp_d
    
    # enumerate
    for idx, val in enumerate(lst_1):
        print 'position: %d, value: %s' % (idx, val)

run_ex_by_flag(ex04)


# EXAMPLE 05-01, insert sort
def ex0501():
    def move_ele_into_sroted_list(test_list, ele_pos):
        tmp_key = test_list[ele_pos]
        sub_pos = ele_pos - 1
     
        if tmp_key >= test_list[sub_pos]:
            return
        while sub_pos >= 0 and test_list[sub_pos] > tmp_key:
            test_list[sub_pos + 1] = test_list[sub_pos]
            sub_pos -= 1
        test_list[sub_pos + 1] = tmp_key
     
    def insert_sort(test_list):
        list_len = len(test_list)
        for idx in xrange(1, list_len):
            move_ele_into_sroted_list(test_list, idx)
            print 'Sorting: ', test_list
                      
        return test_list
       
    my_list = [13, 5, 43, 22, 11, 67, 43, 70, 39, 2]
    print 'Before sort:', my_list
    insert_sort(my_list)
    print 'After sort: ', my_list

run_ex_by_flag(ex0501)


# EXAMPLE 05-02, bubble sort
def ex0502():
    def move_max_val_to_end_by_bubble_com(test_list, end_pos):
        is_exchanged = False
        for j in xrange(end_pos):
            if test_list[j] > test_list[j + 1]:
                test_list[j], test_list[j + 1] = test_list[j + 1], test_list[j]
                is_exchanged = True
     
        return is_exchanged
     
    def bubble_sort(test_list):
        list_len = len(test_list)
        for i in xrange(list_len - 1):
            is_exchanged = move_max_val_to_end_by_bubble_com(test_list, (list_len - 1 - i))
            print 'Sorting: ', test_list
            if not is_exchanged:
                break
     
        return test_list
     
    my_list = [13, 5, 22, 43, 11, 67, 43, 70, 2, 39]
    print 'Before sort:', my_list
    bubble_sort(my_list)
    print 'After sort: ', my_list

run_ex_by_flag(ex0502)


# EXAMPLE 06, quick sort
def ex06():
    def quick_sort(test_list, start_pos, end_pos):
        if start_pos >= end_pos:
            return test_list
         
        tmp_key = test_list[start_pos]
        low = start_pos
        high = end_pos
         
        while low < high:
            while low < high and tmp_key <= test_list[high]:
                high -= 1
            test_list[low] = test_list[high]
            while low < high and tmp_key >= test_list[low]:
                low += 1
            test_list[high] = test_list[low]
        test_list[low] = tmp_key  # low == high
        print 'Sorting: ', test_list
         
        quick_sort(test_list, start_pos, (low - 1))
        quick_sort(test_list, (low + 1), end_pos)
         
        return test_list
     
    my_list = [13, 5, 22, 43, 11, 67, 43, 70, 2, 39]
    print 'Before sort:', my_list
    quick_sort(my_list, 0, (len(my_list) - 1))
    print 'After sort: ', my_list

run_ex_by_flag(ex06)


# EXAMPLE 07, select sort
def ex0701():
    def select_sort_01(test_list):
        # get min value in start by select
        list_len = len(test_list)
        for i in xrange(list_len - 1):
            for j in xrange((i + 1), list_len):
                if test_list[i] > test_list[j]:
                    test_list[i], test_list[j] = test_list[j], test_list[i]
            print 'Sorting: ', test_list
          
        return test_list

    my_list = [13, 5, 22, 43, 11, 67, 43, 70, 2, 39]
    print 'Before sort:', my_list
    select_sort_01(my_list)
    print 'After sort: ', my_list

run_ex_by_flag(ex0701)


def ex0702():
    def select_sort_02(test_list):
        list_len = len(test_list)
        for i in xrange(list_len - 1):
            min_idx = i
            for j in xrange((i + 1), list_len):
                if test_list[min_idx] > test_list[j]:
                    min_idx = j
            test_list[i], test_list[min_idx] = test_list[min_idx], test_list[i]
            print 'Sorting: ', test_list
          
        return test_list
  
    my_list = [13, 5, 22, 43, 11, 67, 43, 70, 2, 39]
    print 'Before sort:', my_list
    select_sort_02(my_list)
    print 'After sort: ', my_list

run_ex_by_flag(ex0702)


# EXAMPLE 08, shell sort
def ex08():
    def shell_sort(test_list):
        list_len = len(test_list)
        group = list_len / 2
      
        while group > 0:
            i = 0
            while i < group:  # iterator for each grouped list
                j = i + group
                while j < list_len:  # iterator for each element in grouped list
                    k = j - group
                    while k >= 0:  # iterator for each element in sub grouped list
                        if test_list[k + group] < test_list[k]:  # insert sort by exchange
                            test_list[k + group], test_list[k] = test_list[k], test_list[k + group]
                        k -= group
                    # end while
                    j += group
                # end while
                i += 1
            # end while
            print 'Sorting: ', test_list
            group = group / 2
        # end while
     
        return test_list
     
    my_list = [13, 5, 22, 43, 11, 67, 43, 70, 2, 39]
    print 'Before sort:', my_list
    shell_sort(my_list)
    print 'After sort: ', my_list

run_ex_by_flag(ex08)


# EXAMPLE 09, import and reload
def ex09():
    import PyDemo04
    PyDemo04.print_message()

    # update PyDemo04
    reload(PyDemo04)
    PyDemo04.print_message()

run_ex_by_flag(ex09)


# EXAMPLE 10, built-in functions
def ex1001():
    print '*' * 20, 'built-in functions'
    import sys
    print 'Module search paths:', sys.path
     
    print 'Defined fields and methods:', dir()
     
    print 'Access global fields:'
    for var in globals():
        if not var.startswith('ex'):
            print var
    
    print 'Access local fields:', locals()

run_ex_by_flag(ex1001)


def ex1002():
    print '*' * 20, 'map() and filter()'
    tmp_ret1 = map(lambda x: x.upper(), ('sentence', 'fragment'))
    print 'Type:', type(tmp_ret1)
    print 'Value:', tmp_ret1
     
    tmp_ret2 = filter(lambda x: (x % 2) == 0, range(10))
    print 'Type:', type(tmp_ret2)
    print 'Value:', tmp_ret2

run_ex_by_flag(ex1002)


# EXAMPLE 11, iteritems()
def ex11():
    mapping = {1:'one', 2:'two', 3:'three', 4:'four'}
    for key, val in mapping.iteritems():
        print 'key:', key, 'value:', val

run_ex_by_flag(ex11)


# EXAMPLE 12, method(*arg)
def ex12():
    def mul(x, y):
        return x * y
     
    tmp_lst = [2, 3]
    print 'results:', mul(*tmp_lst)

run_ex_by_flag(ex12)


# EXAMPLE 13, division
def ex13():
    a = 1
    print a / 2, a / float(2)
    
    # import from beginning of file: 
    # from __future__ import division
    b = 1
    print b // 2, b / 2

run_ex_by_flag(ex13)


# EXAMPLE 14, isinstance
def ex14():
    tmp_str = 'test'
    print 'Type:', type(tmp_str)
    if isinstance(tmp_str, basestring):
        print 'Type is string.'

    tmp_lst = [1, 2, 3]
    if isinstance(tmp_lst, (list, tuple)):
        print 'Type is collection.'

run_ex_by_flag(ex14)


# EXAMPLE 15, get char count in string
# tmp_str = 'abracadabra'
# freqs = {}
# for ch in tmp_str:
#     if ch in freqs:
#         freqs[ch] += 1
#     else:
#         freqs[ch] = 1
# 
# for key, val in freqs.iteritems():
#     print 'key: ', key, 'count: ', val


# EXAMPLE 16, print map
# tmp_map = {'a':'testa', 'b':'testb', 'intc':1}
# print 'map values: %(a)s, %(b)s, %(intc)d' % tmp_map


# EXAMPLE 17, iterator
# 1. loop on iterator
# tmp_lst = ['a', 'b', 'c']
# tmp_iterator = iter(tmp_lst)
# print 'Type:', type(tmp_iterator)
# 
# print 'Elements:'
# try:
#     while 1:
#         print next(tmp_iterator)
# except StopIteration, e:
#     print 'No more elements.'

# 2. iterator to dict
# tmp_lst = [('Italy', 'Rome'), ('France', 'Paris'), ('US', 'Washington DC')]
# tmp_iterator = iter(tmp_lst)
# print 'Type:', type(tmp_iterator)
# print dict(tmp_iterator)

# 3. iterator on file
# import os
# f_path = os.path.join(os.getcwd(), 'zjunittest.log')
# with open(f_path, 'r') as tmp_f:
#     for line in tmp_f:
#         print line.strip('\r\n')


# EXAMPLE 18
# 1, Generator expression, List comprehension
# line_list = ['  line 1\n', 'line 2  \n']
#   
# # Generator expression -- returns generator
# stripped_iter = (line.strip() for line in line_list)
# print 'Type: ', type(stripped_iter)
# for item in stripped_iter:
#     print 'item:', item
# print 'Value as tuple: ', tuple(stripped_iter)
#   
# # List comprehension -- returns list
# stripped_list = [line.strip() for line in line_list]
# print 'Type: ', type(stripped_list)
# print 'Value: ', stripped_list

# 2, range and xrange
# print 'range type:', type(range(10))
# print 'xrange type:', type(xrange(10))


# EXAMPLE 19, lambda
# build_assign = lambda name, value: name + '=' + value
# print build_assign('key_test', 'value_test')


# EXAMPLE 20, python OO
# class Person(object):
#     """ class for test, Person """
#      
#     address = '=> China'
#      
#     @classmethod
#     def myNation(cls):
#         print 'Address: ' + cls.address
#  
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
#  
#     # for print
#     def __str__(self):
#         return 'Name: %s, Age: %d' % (self.name, self.age)
#  
#     def sayHello(self):
#         return 'Hello!'
# # class Person, end
#  
# class Tester(Person):
#     """ class for test, Tester inherit from Person """
#      
#     address = '=> China WuHan'
#      
#     def __init__(self, name, age, company):
#         Person.__init__(self, name, age)
#         self.company = company
#         self.__salary = 0  # private
#         self.__skills = ['Java', 'C++', 'Python', 'JS']
#  
#     def __iter__(self):
# #         return iter(self.__skills)
#         return (v for v in self.__skills)
#  
#     # override
#     def sayHello(self):
#         tmp_list = [Person.sayHello(self), 'I am a tester.']
#         return ' '.join(tmp_list)
#  
#     def setSalary(self, salary):
#         self.__salary = salary
#  
#     def getSalary(self):
#         return self.__salary
# # class Tester, end
#  
# p = Person('henry', 27)
# Person.myNation()
# print p
# print p.sayHello()
#  
# t = Tester('vieira', 29, 'ibm')
# t.setSalary(5000)
# Tester.myNation()
# print t
# print t.sayHello()
# print 'Salary:', t.getSalary()
#  
# print 'Skills:'
# for item in t:
#     print item
#  
# print 'Document:', t.__doc__
# print 'Fields:', t.__dict__
# print t.__module__
# print t.__class__


if __name__ == '__main__':

    print '%s_%s done!' % (os.path.basename(__file__), __name__)
