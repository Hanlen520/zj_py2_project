# -*- coding: utf-8 -*-
'''
Created on 2017-4-2

@author: Vieira
'''

# EXAMPLE 01, method override
# def my_func(name):
#     print 'Hello,', name
# 
# def deco_func(func):
#     print 'in deco func'
#     
#     def in_deco_func(name):
#         print'in in_deco_func'
#         func(name)
# 
#     return in_deco_func
# # end deco_func()
# 
# # 1
# my_func('Test')
# print '*' * 30
# 
# my_func = deco_func(my_func)
# my_func('test override')
# print '*' * 30
# 
# # 2
# @deco_func
# def my_new_func(name):
#     print 'New, hello,', name
# 
# my_new_func('test @deco')


# EXAMPLE 02, method override in class
# class OverrideTest(object):
# 
#     def check(self):
#         ''' only be invoked at first time'''
#         print 'check Invoked'
#         self.check = self.check_post  # re-assign
# 
#     def check_post(self):
#         print 'check_post Invoked'
# 
# my_test = OverrideTest()
# for i in xrange(5):
#     my_test.check()


# EXAMPLE 03, get modules name
# import os, sys, re
#  
# def get_modules_name(file_path):
#     '''
#     input argv from command line:
#     >>> python PyDemo06.py __init__.py
#     >>> python PyDemo06.py ..\ZJPyUtils\__init__.py
#     '''
#     dir_path = os.path.abspath(os.path.dirname(file_path))
#     tmp_files = os.listdir(dir_path)
#     pys = re.compile('.py$', re.IGNORECASE)
#     tmp_files = filter(pys.search, tmp_files)
#     return map(lambda f: os.path.splitext(f)[0], tmp_files)
#      
# print get_modules_name(sys.argv[1])


# EXAMPLE 04, == and is
# tmp_lst1 = [1, 2, 3]
# tmp_lst2 = [1, 2, 3]
# print 'tmp_lst1 == tmp_lst2:', tmp_lst1 == tmp_lst2  # compare content
# print 'tmp_lst1 is tmp_lst2:', tmp_lst1 is tmp_lst2  # compare reference value
# 
# # short string is shared
# tmp_str1 = 'test'
# tmp_str2 = 'test'
# print 'tmp_str1 == tmp_str2:', tmp_str1 == tmp_str2
# print 'tmp_str1 is tmp_str2:', tmp_str1 is tmp_str2


# EXAMPLE 05, *args, **kwargs, *lst
# # 1
# def my_print_args(*args):
#     print 'Type:', type(args)
#     print 'Value:', args
# 
# my_print_args('str1', 'str2', 1, 2)
# 
# # 2
# def my_print_kwargs(**kwargs):
#     print 'Type:', type(kwargs)
#     for key, value in kwargs.iteritems():
#         print 'key: %s, value: %s' % (key, value)
# 
# my_print_kwargs(str1='test1', str2='test2')
# 
# # 3
# def my_print_three_lst_ele(ele1, ele2, ele3):
#     print 'ele1 = %s, ele2 = %s, ele3 = %s' % (ele1, ele2, ele3)
# 
# tmp_lst = ['str1', 'str2', 'str3']
# my_print_three_lst_ele(*tmp_lst)


# EXAMPLE 06, *args, **kwargs in decorate
# def deco(func):
#     def _deco(*args, **kwargs):
#         print 'before %s called.' % func.__name__
#         ret = func(*args, **kwargs)
#         print'after %s called. result: %s' % (func.__name__, ret)
#         return ret
#     return _deco
# 
# @deco
# def my_func(a, b):
#     print 'myfunc(%s,%s) called.' % (a, b)
#     return a + b
# 
# @deco
# def my_func2(a, b, c):
#     print 'myfunc2(%s,%s,%s) called.' % (a, b, c)
#     return a + b + c
# 
# my_func(1, 2)
# print '*' * 40
# my_func(3, 4)
# print '*' * 40
# my_func2(1, 2, 3)
# print '*' * 40
# my_func2(3, 4, 5)


# EXAMPLE 07, RegExp basic
# import re
# 
# # 1, match() and search()
# # re.match() match from beginning
# # re.search() match from anywhere
# print re.match('c', 'abcdef')
# print re.search('c', 'abcdef')
# print re.match('a', 'abcdef')
# print re.search('^a', 'abcdef')
# print '*' * 40
# 
# # 2, if found, return match object; else, return None
# m = re.search('abcd', '1abcd2abcd')
# if m is not None:
#     print 'Value:', m.group()
#     print 'Start index:', m.start()
#     print 'End index', m.end()
# print '*' * 40
# 
# # 3, findall(), finditer(), split()
# print re.findall('(\W+)d', '...dwords, words...d')  # return list
# print re.finditer('(\W+)d', '...dwords, words...d')  # return iterator
# 
# print re.split('[a-z]', '0A3b9z')
# print re.split('[a-z]', '0A3b9z', flags=re.IGNORECASE)
# print '*' * 40
# 
# # 4, group()
# m1 = re.match('(\w+) (\w+)', 'abcd efgh, chaj')
# print m1.group()  # default as m1.group(0)
# print m1.group(1)
# print m1.group(2)
# print m1.group(1, 2)
# print m1.groups()
# print '*' * 40
# 
# m2 = re.match('(?P<first_name>\w+) (?P<last_name>\w+)', 'sam lee')
# print 'first name:', m2.group('first_name')
# print 'last name', m2.group('last_name')
# print m2.groupdict()
# print '*' * 40


# EXAMPLE 08, __slots__ in class
# # 1, with __slots__
# class SlotTest(object):
#     
#     __slots__ = ('name', 'age')
#     
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
# 
#     def getName(self):
#         return self.name
#     
#     def getAge(self):
#         return self.age
# # end class
# 
# st = SlotTest('henry', 25)
# st.age = 27
# print 'name: %s, age: %d' % (st.name, st.age)
# try:
#     st.score = 80
#     print 'score:', st.score
# except AttributeError, e:
#     print 'Error:', e.message
# print '*' * 40
# 
# # 2, without __slots__
# class MyTest(object):
# 
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
# 
#     def getName(self):
#         return self.name
#     
#     def getAge(self):
#         return self.age
# 
# mytest = MyTest('henry', 25)
# mytest.age = 27
# print 'name: %s, age: %d' % (mytest.name, mytest.age)
# mytest.score = 80
# print 'score:', mytest.score


# EXAMPLE 09, reflection by module 'inspect'
# import inspect
# import sys
# 
# print 'isbuiltin:', inspect.isbuiltin(abs)
# print 'ismodule:', inspect.ismodule(sys)
# 
# class MyTestCls(object):
#     pass
# print 'isclass:', inspect.isclass(MyTestCls)
# 
# def MyTestMtd():
#     pass
# print 'isfunction:', inspect.isfunction(MyTestMtd)


if __name__ == '__main__':

    import os
    print '%s done!' % os.path.basename(__file__)
    pass
