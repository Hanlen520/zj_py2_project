# -*- coding: utf-8 -*-
'''
Created on 2016-7-13

@author: zhengjin
'''

import os

# EXAMPLE 01
# import platform
# system = platform.system()
# if system == 'Windows':
#     print 'Win'
# else:
#     print 'Linux'


# EXAMPLE 02
# if 'ANDROID_HOME' in os.environ:
#     print os.environ['ANDROID_HOME']


# EXAMPLE 03
# import time
# print time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))


# EXAMPLE 04
# import json
# 
# json_data = '{"total":239,"row":[{"code":"001","name":"\u4e2d\u56fd","addr":"Address 11","col4":"col4 data"},{"code":"002","name":"Name 2","addr":"Address 12","col4":"col4 data"}]}'
# json_arr = json.loads(json_data,encoding='utf-8')
# print json_arr['total']
# print json_arr['row'][0]['code']
# 
# for key in json_arr.keys():
#     print type(key)


# EXAMPLE 05
# str = u'test'
# print type(str)
# print type(str.encode('utf-8'))


# EXAMPLE 06
# import urllib2
# 
# url = 'http://apis.baidu.com/apistore/weatherservice/citylist?cityname=%E6%9C%9D%E9%98%B3'
# 
# req = urllib2.Request(url)
# req.add_header("apikey", "11c756e31e9bed863a743ccff784ddeb")
# 
# resp = urllib2.urlopen(req)
# content = resp.read()
# if(content):
#     print(content)
# else:
#     print 'Error.'


# EXAMPLE 07
# import re
#  
# str = '-28C'
# print re.findall(r'\d+', str)
# print re.findall(r'-(\d+)C', str)


# EXAMPLE 08
# city_id1 = 1
# city_name1 = 'city1'
# city_id2 = 2
# city_name2 = 'city2'
#  
# city_list = {}
# city_list[city_id1] = city_name1
# city_list[city_id2] = city_name2
#  
# for k,v in city_list.items():
#     print 'key: %s' %k
#     print 'value: %s' %v


# EXAMPLE 09
# dic = {'1':'a','3':'c','2':'b'}
# items = dic.items()
# items.sort()
# print items
# for k,v in items:
#     print k
#     print v
# 
# for k,v in sorted(dic.items(),key=lambda d:d[0]):
#     print k


# EXAMPLE 10
# i = 1
# i += 2
# print i


# EXAMPLE 11
# str = '\u5317\u4eac'
# print type(str)
# str_f = str.decode('utf-8').encode('gbk')
# print type(str_f)
# str_f = str.decode('unicode_escape')
# print str_f


# EXAMPLE 12
# import os
# content = ''
# with open(os.path.join(os.getcwd(), 'zjunittest.log')) as f:
#     content = f.read()
# print content


# EXAMPLE 13
# def my_print():
#     print 'it is a test.'
#     
# def main(fn):
#     print 'run function: %s' %fn.__name__
#     fn()
#
#    main(my_print)


# EXAMPLE 14
# import re
# str1 = '嫁个老公过日子（更新至24集）'
# str2 = '幸福满屋（全30集）'
# res = re.search('[至全](\d+)集',str2)
# print res.group(1)


# EXAMPLE 15
# str = 'test'
# print str[-1]  # print last word


# EXAMPLE 16
# cmd1 = 'ping 172.17.5.106'
# p = os.popen(cmd1)
# print type(p)
# print len(p.readlines())


# EXAMPLE 17
# g_var = 'init'
# def print_var():
#     print 'Output:', g_var
# 
# print_var()


# EXAMPLE 18
# class A(object):
#     def __init__(self):
#         self.__private()
#         self.public()
#     def __private(self):
#         print 'A.__private()'
#     def public(self):
#         print 'A.public()'
# 
# class B(A):
# #     def __init__(self):
# #         self.__private()
# #         self.public()
#     def __private(self):
#         print 'B.__private()'
#     def public(self):
#         print 'B.public()'
# 
# # print '\n'.join(dir(A)), '\n'
# # print '\n'.join(dir(B)), '\n'
# b = B()


# EXAMPLE 19
# import subprocess
# print subprocess.call(["cmd"])

# p = subprocess.Popen('cmd',stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
# p.communicate()
# print p.stdout.read()
# print p.communicate(input='adb devices')
# print p.communicate(input='java -version')[0], '/n'
# print 'Output:',p.returncode


# EXAMPLE 20
# print Python module search path
# import sys
# print sys.path


# EXAMPLE 21
# var_global = 'test1'
# def my_print():
#     var_local = 'test2'
#     print var_local
#     print globals()  # print global vars can be access
#     print locals()  # print local vars can be access
#     
# my_print()


# EXAMPLE 22
# from sys import stdout 
# str1 = 'hello, zheng jin '
# str2 = 'it test.\n'
# stdout.write(str1)
# stdout.write(str2)


# EXAMPLE 23-1
# def sortby(somelist, n):
#     nlist = [(x[n], x) for x in somelist]
#     nlist.sort()
#     return [val for (key, val) in nlist]
# 
# def sortby_inplace(somelist, n):
#     somelist[:] = [(x[n], x) for x in somelist]
#     somelist.sort()
#     somelist[:] = [val for (key, val) in somelist]
#     return
# 
# somelist = [(1, 2, 'def'), (2, -4, 'ghi'), (3, 6, 'abc')]
# somelist.sort()
# print somelist
# print sortby(somelist, 2)

# EXAMPLE 23-2
# import operator
# 
# somelist = [(1, 2, 'def'), (2, -4, 'ghi'), (3, 6, 'abc')]
# somelist.sort(key=operator.itemgetter(1))
# print somelist


# EXAMPLE 24
# oldlist = ['test1', 'test2']
# newlist = []

# for word in oldlist:
#     newlist.append(word.upper())
# print newlist

# newlist = [val.upper() for val in oldlist]
# print newlist

# newlist = map(str.upper, oldlist)
# print newlist


# EXAMPLE 25
# def generate_ints(n):
#     for i in xrange(n):
#         yield i
# 
# gen = generate_ints(3)
# print gen.next()
# print gen.next()
# print next(gen)


# EXAMPLE 26
# def my_upper(s):
#     return s.upper()
#     
# li = map(my_upper, ['hello', 'zhengjin'])
# print li
# 
# print [my_upper(val) for val in ['hello', 'zhengjin']]


# EXAMPLE 27
# def is_even(x):
#     return (x % 2) == 0
# 
# li = filter(is_even, range(10))
# print li
# 
# print [val for val in range(10) if is_even(val)]


# EXAMPLE 28
# import functools
# items = ['11', '13', '15']
# def my_combine(a, b):
#     return 0, int(a[1]) + int(b[1])

# total = functools.reduce(my_combine, items)[1]
# print total

# total = 0
# for a, b in items:
#     print 'a =', a
#     print 'b =', b
#     total += int(b)
# print total

# total = sum(int(b) for a,b in items)
# print total


# EXAMPLE 29
# def parms_test(*argv):
#     print 'Parms length:', len(argv)
#     print 'Parms:', argv
#     print 'Parms %s' % str(argv)
#     
#     for parm in argv:
#         print 'Parm:', parm
#     
#     print 'Parms join:', ','.join(argv)
#         
# parms_test('parm1', 'parm2', '中文')


# EXAMPLE 30
# total_time = 45;
# print '%d h, %d mins' % (int(total_time / 60), int(total_time % 60))


if __name__ == '__main__':
    # EXAMPLE 17
#     g_var = 'update'
#     print_var()
    
    print("%s done!" %os.path.basename(__file__))
    pass