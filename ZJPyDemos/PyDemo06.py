# -*- coding: utf-8 -*-
'''
Created on 2017-4-2

@author: Vieira
'''

import os

from PyDemo01 import run_ex_by_flag

# EXAMPLE 01, method override
def ex01():
    def my_func(name):
        print 'Hello,', name

    print '*' * 30, 'case 1'
    my_func('Test')

    print '*' * 30, 'case 2'
    def deco_func(func):
        print 'in deco func'
        def in_deco_func(name):
            print'in in_deco_func'
            func(name)

        return in_deco_func

    my_func = deco_func(my_func)
    my_func('test override')

    print '*' * 30, 'case 3'
    @deco_func
    def my_new_func(name):
        print 'New, hello,', name

    my_new_func('test @deco')

run_ex_by_flag(ex01)


# EXAMPLE 02, method override in class
class OverrideTest(object):
 
    def check(self):
        ''' only be invoked at first time'''
        print 'check Invoked'
        self.check = self.check_post  # re-assign
 
    def check_post(self):
        print 'check_post Invoked'

def ex02():
    my_test = OverrideTest()
    my_test.check()
    my_test.check()
    my_test.check()

run_ex_by_flag(ex02)


# EXAMPLE 03, get modules name
def ex03():
    import sys, re

    def get_modules_name(file_name):
        '''
        input argv from command line:
        >>> python PyDemo06.py __init__.py
        >>> python PyDemo06.py ..\ZJPyUtils\__init__.py
        '''
        dir_path = os.path.abspath(os.path.dirname(file_name))
        tmp_files = os.listdir(dir_path)
        pys = re.compile('.py$', re.IGNORECASE)
        tmp_files = filter(pys.search, tmp_files)
        return map(lambda f: os.path.splitext(f)[0], tmp_files)

    print get_modules_name(sys.argv[1])

run_ex_by_flag(ex03)


# EXAMPLE 04, == and is
def ex04():
    tmp_lst1 = [1, 2, 3]
    tmp_lst2 = [1, 2, 3]
    print 'tmp_lst1 == tmp_lst2:', tmp_lst1 == tmp_lst2  # compare content
    print 'tmp_lst1 is tmp_lst2:', tmp_lst1 is tmp_lst2  # compare reference value

    # short string is shared
    tmp_str1 = 'test'
    tmp_str2 = 'test'
    print 'tmp_str1 == tmp_str2:', tmp_str1 == tmp_str2
    print 'tmp_str1 is tmp_str2:', tmp_str1 is tmp_str2

run_ex_by_flag(ex04)


# EXAMPLE 05, *args, **kwargs, *lst
def ex05():
    # 1
    def my_print_args(*args):
        print 'Type:', type(args)
        print 'Value:', args
    my_print_args('str1', 'str2', 1, 2)
     
    # 2
    def my_print_kwargs(**kwargs):
        print 'Type:', type(kwargs)
        for key, value in kwargs.iteritems():
            print 'key: %s, value: %s' % (key, value)
    my_print_kwargs(str1='test1', str2='test2')
     
    # 3
    def my_print_three_lst_ele(ele1, ele2, ele3):
        print 'ele1 = %s, ele2 = %s, ele3 = %s' % (ele1, ele2, ele3)
     
    tmp_lst = ['str1', 'str2', 'str3']
    my_print_three_lst_ele(*tmp_lst)

run_ex_by_flag(ex05)


# EXAMPLE 06, *args, **kwargs in decorate
def ex06():
    def deco(func):
        def _deco(*args, **kwargs):
            print 'before %s called.' % func.__name__
            ret = func(*args, **kwargs)
            print'after %s called.' % (func.__name__)
            return ret
        return _deco

    @deco
    def my_func(a, b):
        print 'myfunc(%s,%s) called.' % (a, b)
        return a + b

    @deco
    def my_func2(a, b, c):
        print 'myfunc2(%s,%s,%s) called.' % (a, b, c)
        return a + b + c

    print 'results: ' + str(my_func(1, 2))
    print '*' * 40
    print 'results:\n', my_func(3, 4)

    print '*' * 40
    print 'results: ' + str(my_func2(1, 2, 3))
    print '*' * 40
    print 'results:\n', my_func2(3, 4, 5)

run_ex_by_flag(ex06)


# EXAMPLE 07, RegExp basic
def ex07():
    import re

    # 1, match() and search()
    # re.match() find from beginning
    # re.search() find from anywhere
    print '*' * 20, 'case 1' 
    print re.match('c', 'abcdef')
    print re.search('c', 'abcdef')
    print re.match('a', 'abcdef')
    print re.search('^a', 'abcdef')

    # 2, if found, return match object; else, return None
    print '*' * 20, 'case 2'
    m = re.search('abcd', '1abcd2abcd')
    if m is not None:
        print 'Value:', m.group()
        print 'Start index:', m.start()
        print 'End index', m.end()

    # 3, findall(), finditer(), split()
    print '*' * 20, 'case 3'
    print re.findall('(\W+)d', '...dwords, words...d')  # return list
    
    tmp_iter = re.finditer('(\W+)d', '...dwords, words...d')  # return iterator
    for item in tmp_iter:
        print 'element:', item.group(0, 1)

    print re.split('[a-z]', '0A3b9z')
    print re.split('[a-z]', '0A3b9z', flags=re.IGNORECASE)

    # 4, group()
    print '*' * 20, 'case 4'
    m1 = re.match('(\w+) (\w+)', 'abcd efgh, chaj')
    print m1.group()  # default as m1.group(0)
    print m1.group(1)
    print m1.group(2)
    print m1.group(1, 2)
    print m1.groups()

    print '*' * 20, 'case 5'
    m2 = re.match('(?P<first_name>\w+) (?P<last_name>\w+)', 'sam lee')
    print 'first name:', m2.group('first_name')
    print 'last name:', m2.group('last_name')
    print m2.groupdict()

run_ex_by_flag(ex07)


# EXAMPLE 08, __slots__ in class
# 1, class without __slots__
class MyTest(object):
  
    def __init__(self, name, age):
        self.name = name
        self.age = age
  
    def getName(self):
        return self.name
      
    def getAge(self):
        return self.age

def ex0801():
    mytest = MyTest('henry', 25)
    mytest.age = 27
    print 'name: %s, age: %d' % (mytest.name, mytest.age)

    # add an attribute dyn
    mytest.score = 80
    print 'score:', mytest.score
    print [attr for attr in dir(mytest) if not attr.startswith('__')]

    # remove an attribute dyn
    del mytest.score
    try:
        print 'score:', mytest.score
    except AttributeError, e:
        print 'Error:', e.message
    print [attr for attr in dir(mytest) if not attr.startswith('__')]

run_ex_by_flag(ex0801)


# 2, class with __slots__
class SlotTest(object):
      
    __slots__ = ('name', 'age')
      
    def __init__(self, name, age):
        self.name = name
        self.age = age
  
    def getName(self):
        return self.name
      
    def getAge(self):
        return self.age

def ex0802():
    st = SlotTest('henry', 25)
    st.age = 27
    print 'name: %s, age: %d' % (st.name, st.age)

    # cannot add an attribute dyn because of __slots__ definition
    try:
        st.score = 80
        print 'score:', st.score
    except AttributeError, e:
        print 'Error:', e.message
    
    # remove an attribute dyn
    del st.age
    try:
        print 'age:' + str(st.age)
    except AttributeError, e:
        print 'Error: get attribute ' + e.message

    print [attr for attr in dir(st) if not attr.startswith('__')]

run_ex_by_flag(ex0802)


# EXAMPLE 09, reflection by module 'inspect'
def ex09():
    import inspect
    import sys
     
    print 'isbuiltin:', inspect.isbuiltin(abs)
    print 'ismodule:', inspect.ismodule(sys)

    class MyTestCls(object):
        pass
    print 'isclass:', inspect.isclass(MyTestCls)

    def MyTestMtd():
        pass
    print 'isfunction:', inspect.isfunction(MyTestMtd)

run_ex_by_flag(ex09)


# EXAMPLE 10, issubclass() and isinstance()
def ex10():
    class MyTestSuper(object):
        pass

    class MyTestChild(MyTestSuper):
        pass

    my_child = MyTestChild()
    print 'isinstance(my_child, MyTestChild):', isinstance(my_child, MyTestChild)
    print 'isinstance(my_child, MyTestSuper):', isinstance(my_child, MyTestSuper)

    print 'issubclass(MyTestChild, MyTestChild):', issubclass(MyTestChild, MyTestChild)
    print 'issubclass(MyTestChild, MyTestSuper):', issubclass(MyTestChild, MyTestSuper)

run_ex_by_flag(ex10)


# EXAMPLE 11, private var in class
class MySuper(object):
     
    def __init__(self):
        print type(self)
        self.__private()  # Private name mangling
        self.public()
 
    def __private(self):  # Private name mangling
        print 'MySuper.__private()'
 
    def public(self):
        print 'MySuper.public()'
# end class

class MySub(MySuper):
     
    def __private(self):
        print 'MyChild.__private()'
 
    def public(self):
        print 'MyChild.public()'
# end class

def ex11():
    def get_own_attributes(in_object):
        return [attr for attr in dir(in_object) if not attr.startswith('__')]

    print 'MySuper attributes:', get_own_attributes(MySuper)
    print 'MyChild attributes:', get_own_attributes(MySub)

    print '*' * 30
    test_sub = MySub()
    print '*' * 30
    print 'child attributes:', get_own_attributes(test_sub)

run_ex_by_flag(ex11)


# EXAMPLE 12, tuple initialize
# tmp_t = 1, 2, 3
# print 'Type:', type(tmp_t)
# print 'Value:', tmp_t
# 
# print 'a=%d, b=%d, c=%d' % tmp_t  # tuple: (1, 2, 3)
# 
# x, y, z = tmp_t
# print 'x=' + str(x), 'y=' + str(y), 'z=' + str(z)


# EXAMPLE 13, sub and modify list
# tmp_lst = ['a', 'b', 'c', 'd']
# for item in tmp_lst[1:]:
#     print 'item:', item
# 
# tmp_lst2 = ['1', '2', '3', '4']
# tmp_lst2.insert(2, 'a')
# print tmp_lst2
#  
# tmp_lst3 = ['1', '2', '3', '4']
# print tmp_lst3[0:2]
# tmp_lst3[0:2] = ['a', 'b', 'c']
# print tmp_lst3
# 
# # print help(list)


# EXAMPLE 14, try except block
# def test_exception():
#     raise Exception('test try except block')
#  
# def stub_function():
#     pass
#  
# # 1
# # try:
# #     test_exception()
# # except Exception, e:
# #     print 'Exception:', e.message
#  
# # 2
# try:
#     test_exception()
# except Exception as ex:
#     print 'Exception:', ex.message
# 
# # 3
# try:
#     stub_function()
# except Exception, e:
#     print 'Exception:', e.message
# else:
#     print 'No error'


# EXAMPLE 15, read ini properties
# import os
# import ConfigParser
#  
# conf_file = ConfigParser.ConfigParser()
# conf_file.read(os.path.join(os.getcwd(), 'conf.ini'))
#  
# confs = {}
# confs['sender'] = conf_file.get('email','sender')
# confs['receiver'] = conf_file.get('email','receiver')
# confs['smtpserver'] = conf_file.get('email','smtpserver')
# confs['username'] = conf_file.get('email','username')
# confs['password'] = conf_file.get('email','password')
#  
# for k,v in confs.iteritems():
#     print 'key=%s, val=%s' % (k, v)


if __name__ == '__main__':

    print '%s done!' % os.path.basename(__file__)
    pass
