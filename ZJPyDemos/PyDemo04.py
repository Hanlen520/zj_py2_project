# -*- coding: utf-8 -*-
'''
Created on 2016-7-13

@author: zhengjin
'''

import os

from PyDemo01 import run_ex_by_flag

# EXAMPLE 01, platform
def ex01():
    import platform
    tmp_system = platform.system()
    print tmp_system
    if tmp_system == 'Windows':
        print 'Win'
    else:
        print 'Linux'
     
    import sys
    print sys.platform

run_ex_by_flag(ex01)


# EXAMPLE 02, os environ vars
def ex02():
    # if 'ANDROID_HOME' in os.environ:
    # if 'ANDROID_HOME' in os.environ.keys():
    if os.environ.has_key('ANDROID_HOME'):
        print os.environ['ANDROID_HOME']

run_ex_by_flag(ex02)


# EXAMPLE 03, get datetime
def ex03():
    import time
    print time.strftime('%Y-%m-%d %H:%M:%S')
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

run_ex_by_flag(ex03)


# EXAMPLE 04, json loads() and dumps()
def ex04():
    import json
        
    json_data_str = '{"data":{"name":"zhengjin", "age":30, "skill":["Java", "Python", "C++"]}, "retCode":"200"}'
    json_arr = json.loads(json_data_str, encoding='utf-8')
    print json_arr['retCode']
    print json_arr['data']['skill'][0]

    json_obj = {'data': {'name': 'zhengjin', 'age': 30, 'skill': ['Java', 'Python', 'C++']}, 'retCode': '200'}
    print str(json_obj)
    json_str = json.dumps(json_obj, encoding='utf-8')
    print json_str

run_ex_by_flag(ex04)


# EXAMPLE 05, str and unicode
def ex05():
    print '*' * 20, 'unicode test'
    unicode_cn = u'中文'
    print 'Type:', type(unicode_cn)
    print 'Type unicode:', isinstance(unicode_cn, unicode)
    print 'Type string:', isinstance(unicode_cn, str)
    print 'Length: %d bytes' % len(unicode_cn)  # get number of cn chars
    print 'Value:', unicode_cn

    print '*' * 20, 'str utf8 test'
    str_utf8_cn = '中文'
    print 'Type:', type(str_utf8_cn)
    print 'Type unicode:', isinstance(str_utf8_cn, unicode)
    print 'Type string:', isinstance(str_utf8_cn, str)
    # '\xe4\xb8\xad\xe6\x96\x87'
    # for utf8, in hex, 3 bytes for one cn char
    print 'Length: %d bytes' % len(str_utf8_cn)
    print 'Value:', str_utf8_cn

    print '*' * 20, 'str gbk test'
    str_gbk_cn = u'中文'.encode('gbk')
    print 'Type:', type(str_gbk_cn)
    print 'Type unicode:', isinstance(str_gbk_cn, unicode)
    print 'Type string:', isinstance(str_gbk_cn, str)
    # for gbk, 2 bytes for one cn char
    print 'Length: %d bytes' % len(str_gbk_cn)
    print 'Value:', str_gbk_cn

    print '*' * 20, 'setdefaultencoding test'
    import sys
    print 'default encode:', sys.getdefaultencoding()
    reload(sys)
    sys.setdefaultencoding('gbk')
    print 'reset encode:', sys.getdefaultencoding()
    print 'Value:', str_gbk_cn.encode('utf-8')  # default decode reset to 'gbk'

    print '*' * 20, 'decode(unicode_escape) test'
    str_unicode_1 = '\u0041'
    print 'Length: %d bytes' % len(str_unicode_1)
    str_unicode_escape = str_unicode_1.decode('unicode_escape')
    print 'Type:', type(str_unicode_escape)
    print 'Length: %d bytes' % len(str_unicode_escape)
    print 'Value:', str_unicode_escape
    
    str_unicode_2 = '\\u4e2d'
    print 'Value:', str_unicode_2.decode('unicode_escape')
    
    # str_unicode_3 = '\\u4fee\\u6539\\u8282\\u70b9\\u72b6\\u6001\\u6210\\u529f'
    str_unicode_3 = '\u4fee\u6539\u8282\u70b9\u72b6\u6001\u6210\u529f'
    print 'Value:', str_unicode_3.decode('unicode_escape')

run_ex_by_flag(ex05)


# EXAMPLE 06, send request
def ex06():
    import urllib2
     
    url = 'http://apis.baidu.com/apistore/weatherservice/citylist?cityname=%E6%9C%9D%E9%98%B3'
    req = urllib2.Request(url)
    req.add_header('apikey', '11c756e31e9bed863a743ccff784ddeb')
     
    resp = urllib2.urlopen(req)
    content = resp.read()
    if(content):
        print(content)
    else:
        print 'Error.'

run_ex_by_flag(ex06)


# EXAMPLE 07, RegExp
def ex07():
    import re
       
    tmp_str = '-28C'
    m = re.search(r'\d+', tmp_str)
    print m.group()
    
    print re.findall(r'\d+', tmp_str)
    print re.findall(r'-?(\d+)C', tmp_str)

run_ex_by_flag(ex07)


# EXAMPLE 08, dict
def ex08():
    city_id1 = 1
    city_name1 = 'city1'
    city_id2 = 2
    city_name2 = 'city2'
       
    city_list = {}
    city_list[city_id1] = city_name1
    city_list[city_id2] = city_name2
       
    for k, v in city_list.iteritems():
        print 'key: %d, value: %s' % (k, v)

run_ex_by_flag(ex08)


# EXAMPLE 09, sort
def ex09():
    tmp_dict = {'1':'a', '3':'b', '2':'c'}
    tmp_kv_items = tmp_dict.items()
    print tmp_kv_items
    
    print 'iterator 1:'
    tmp_kv_items.sort()
    for item in tmp_kv_items:
        print item

    print 'iterator 2:'
    for k, v in sorted(tmp_dict.items(), key=lambda x : x[1]):
        print k, v

run_ex_by_flag(ex09)


# EXAMPLE 10, +=
def ex10():
    i = 1
    i += 2
    print i

run_ex_by_flag(ex10)


# EXAMPLE 11, decode('unicode_escape')
def ex11():
    print '*' * 20, 'unicode case1'
    tmp_u = u'\u5317\u4eac'
    print type(tmp_u)
    print tmp_u
    print tmp_u.encode('utf-8')

    print '*' * 20, 'unicode case2'
    tmp_str = '\u5317\u4eac'
    print type(tmp_str)
    print tmp_str

    tmp_str_u = tmp_str.decode('unicode_escape')
    print type(tmp_str_u)
    print tmp_str_u

run_ex_by_flag(ex11)


# EXAMPLE 12, with block
def ex12():
    with open(os.path.join(os.getcwd(), 'zjunittest.log')) as f:
        content = f.read()
        print content

run_ex_by_flag(ex12)


# EXAMPLE 13, fn.__name__
def ex13():
    def my_print():
        print 'it is a print test.'
          
    def main(fn):
        print 'run function:', fn.__name__
        fn()
     
    main(my_print)

run_ex_by_flag(ex13)


# EXAMPLE 14, RegExp
def ex14():
    import re
    str1 = '嫁个老公过日子（更新至24集）'
    str2 = '幸福满屋（全30集）'

    m1 = re.search('[至全](\d+)集', str1)
    print dir(m1)
    print m1.group(1)

    m2 = re.search('[至全](\d+)集', str2)
    print m2.group(1)

run_ex_by_flag(ex14)


# EXAMPLE 15, print last word
def ex15():
    tmp_str = 'test'
    print tmp_str[-1]

run_ex_by_flag(ex15)


# EXAMPLE 16, os.popen()
def ex16():
    cmd = 'ping 172.17.5.106'
    ret_f = os.popen(cmd)  # async
    print type(ret_f)
    print isinstance(ret_f, file)

    for line in ret_f:
        print line.rstrip('\r\n').decode('gbk')

run_ex_by_flag(ex16)


# EXAMPLE 17, class inherit
def ex17():
    class A(object):
        
        def __init__(self):
            self.__private()
            self.public()

        def __private(self):
            print 'A.__private()'
        
        def public(self):
            print 'A.public()'
     
    class B(A):

        def __init__(self):
            A.__init__(self)
            self.__private()
            self.public()
        
        def __str__(self):
            return 'class B'
     
        def __private(self):
            print 'B.__private()'
        
        def public(self):
            print 'B.public()'

    # dir() => for a class object: its attributes, and recursively the attributes of its bases
    print '\n'.join(dir(B))

    b = B()
    print b

run_ex_by_flag(ex17)


# EXAMPLE 18, print module search paths
def ex18():
    import sys
    print sys.path

run_ex_by_flag(ex18)


# EXAMPLE 19, globals() and locals()
var_global = 'test'
def ex19():
    print '*' * 20, 'case 1'
    print globals()['os']

    print '*' * 20, 'case 2'
    from os.path import exists
    if exists(r'd:\debug.keystore'):
        print 'file exist'
    print 'ex19() local vars:', locals()['exists']

    print '*' * 20, 'case 3'
    var_ex19_global = 'test1'
    print var_ex19_global
    def my_print_01():
        var_local = 'test2'
        print var_local
        print 'my_print_01() local vars:', locals()
    my_print_01()

    print '*' * 20, 'case 4'
    def my_print_02():
        var_local = 'test3'
        print var_local
        print var_ex19_global
        print 'my_print_02() local vars:', locals()
    my_print_02()

    print '*' * 20, 'case 5'
    def my_print_03():
        print 'global vars:'
        for k, v in globals().iteritems():
            if k.startswith('__') or k.startswith('ex'):
                continue
            print 'var: %s, value: %s' % (k, v)
    my_print_03()

run_ex_by_flag(ex19)


# EXAMPLE 20, stdout
def ex20():
    from sys import stdout 
    str1 = 'hello, zheng jin '
    str2 = 'it\'s test.\n'
    stdout.write(str1)
    stdout.write(str2)

run_ex_by_flag(ex20)


# EXAMPLE 21-1, sort
def ex2101():
    def sortby(somelist, n):
        nlist = [(x[n], x) for x in somelist]
        nlist.sort()
        return [val for (key, val) in nlist]

    def sortby_inplace(somelist, n):
        somelist[:] = [(x[n], x) for x in somelist]
        somelist.sort()
        somelist[:] = [val for (key, val) in somelist]

    somelist = [(1, 2, 'def'), (2, -4, 'ghi'), (3, 6, 'abc')]
    tmp_lst_cp1 = somelist[:]
    tmp_lst_cp2 = somelist[:]
    tmp_lst_cp3 = somelist[:]

    somelist.sort()
    print somelist

    tmp_lst_cp1.sort(key=lambda x:x[2], reverse=False)
    print tmp_lst_cp1

    print sortby(tmp_lst_cp2, 2)

    sortby_inplace(tmp_lst_cp3, 2)
    print tmp_lst_cp3

run_ex_by_flag(ex2101)


# EXAMPLE 21-2, sort
def ex2102():
    import operator
    somelist = [(1, 2, 'def'), (2, -4, 'ghi'), (3, 6, 'abc')]
    somelist.sort(key=operator.itemgetter(2))
    print somelist

run_ex_by_flag(ex2102)


# EXAMPLE 22, iterator
def ex22():
    oldlist = ['java', 'javascript', 'python']
    newlist = []

    print '*' * 20, 'case 1'
    for word in oldlist:
        newlist.append(word.upper())
    print newlist
    del newlist[:]

    print '*' * 20, 'case 2'
    upper = str.upper
    append = newlist.append
    for word in oldlist:
        append(upper(word))
    print newlist
    del newlist[:]

    print '*' * 20, 'case 3'
    newlist = map(str.upper, oldlist)
    print newlist
    del newlist[:]

    print '*' * 20, 'case 4'
    newlist = [val.upper() for val in oldlist]
    print newlist

run_ex_by_flag(ex22)


# EXAMPLE 23, iterator
def ex23():
    def my_upper(s):
        return s.upper()
     
    tmp_lst = ['java', 'javascript', 'python']
    print [my_upper(val) for val in tmp_lst]
    print map(my_upper, tmp_lst)

run_ex_by_flag(ex23)


# EXAMPLE 24, filter()
def ex24():
    def is_even(x):
        return (x % 2) == 0

    print '*' * 20, 'case 1'
    tmp_lst = range(10)
    print type(tmp_lst)
    print tmp_lst
    
    print '*' * 20, 'case 2'
    tmp_gen = xrange(10)
    print type(tmp_gen)

    print [val for val in tmp_gen if val % 2 == 0]
    print [val for val in tmp_gen if is_even(val)]
    print filter(is_even, tmp_gen)

run_ex_by_flag(ex24)


# EXAMPLE 25, generator
# # 1, yield
# def generate_ints(n):
#     for i in xrange(n):
#         yield i
# 
# my_gen1 = generate_ints(10)
# print 'Type:', type(my_gen1)
# for ele in my_gen1:
#     print 'Element:', ele
#  
# my_gen2 = generate_ints(3)
# print 'Type:', type(my_gen2)
# print my_gen2.next()
# print my_gen2.next()
# print next(my_gen2)
# print next(my_gen2)  # StopIteration

# # 2, pass value by send()
# def counter(max_value):
#     i = 0
#     while i < max_value:
#         val = (yield i)
#         if val is not None:
#             i = val
#         else:
#             i += 1
#  
# my_gen = counter(10)
# print 'Type:', type(my_gen)
#  
# print my_gen.next()
# print my_gen.next()
# print my_gen.send(8)
# print next(my_gen)
# print next(my_gen)


# EXAMPLE 26, iterator
# tmp_items = ['11', '13', '15']
#
# import functools
# def my_combine(a, b):
#     print 'a:', a
#     print 'b:', b
#     return 0, int(a[1]) + int(b[1])
# 
# total = functools.reduce(my_combine, tmp_items)
# print total[1]

# total = 0
# for a, b in tmp_items:
#     print 'a =', a
#     print 'b =', b
#     total += int(b)
# print total

# # total = sum([int(b) for a,b in tmp_items])
# total = sum(int(b) for a,b in tmp_items)
# print total


# EXAMPLE 27, *argv
# def parms_test(*argv):
#     print 'Parms length:', len(argv)
#     print 'Parms:', argv
#     print 'Parms %s' %str(argv)
#      
#     for parm in argv:
#         print 'Parm:', parm
#      
#     print 'Parms join:', ','.join(argv)
#          
# parms_test('parm1', 'parm2', '中文')


# EXAMPLE 28, time format
# total_time = 145
# print '%d h, %d mins' %(int(total_time / 60), int(total_time % 60))


# EXAMPLE 29, invoked from PyDemo05, EXAMPLE 09 import and reload
# print 'code to be run when import or reload.'
def print_message():
    print 'import and reload test.'


if __name__ == '__main__':
    
    print '%s done!' % os.path.basename(__file__)
