# -*- coding: utf-8 -*-
'''
Created on 2014/9/24

@author: zhengjin
'''

import os
# from __future__ import division

# EXAMPLE 01, struct
is_ex01_run = False
if is_ex01_run:
    import struct
    print(struct.calcsize('P'))


# EXAMPLE 02, collection
def ex02():
    tmp_tup = ('t')
    print tmp_tup
     
    tmp_arr = ['a']
    print tmp_arr[0]
     
    tmp_dic = {'name':'henry'}
    tmp_dic['heigh'] = '173'
    print tmp_dic

is_ex02_run = False
if is_ex02_run:
    ex02()


# EXAMPLE 03, file append
def ex03():
    f = open(r'd:\test.log', 'a')
    name1 = 'henry'
    name2 = 'vieira'
    f.write('test %s \n' % (name1))
    f.write('test %s' % (name2))
    f.close()

is_ex03_run = False
if is_ex03_run:
    ex03()


# EXAMPLE 04, print float
is_ex04_run = False
if is_ex04_run:
    import math
    print '%.3f' % math.pi
    print '%.3f' % (5.0 / 4.0)


# EXAMPLE 05, split
is_ex05_run = False
if is_ex05_run:
    tmp_path = 'FramesLog_01_Baseline.log'
    print tmp_path.split('.')[0]


# EXAMPLE 06, join
def ex06():
    my_list = ['1', '2', '3', '4', '5']
    print' : '.join(my_list)

    sub_len = int(round(len(my_list) * 0.5))
    print my_list[0:sub_len]

is_ex06_run = False
if is_ex06_run:
    ex06()


# EXAMPLE 07, subprocess
def ex07():
    import subprocess
    p = subprocess.Popen('java -version')
    p.wait()

is_ex07_run = False
if is_ex07_run:
    ex07()


# EXAMPLE 08, os.path
def ex08():
    file_path = 'e:\log.txt'
    if not os.path.exists(file_path):
        print 'The file (%s) is not found!' % file_path

is_ex08_run = False
if is_ex08_run:
    ex08()


# EXAMPLE 09, if
is_ex09_run = False
if is_ex09_run:
    if 1 == 1 and 2 == 2:
        print 'pass'


# EXAMPLE 10, file write
# import os
# version_num = "1.0.0.59"
# saved_apk_dir = os.path.join(r"E:\apk_build", version_num)
# print saved_apk_dir
#
# f = open(r"d:\logtest.txt", "w")
# f.write("hello world")
# f.close()


# EXAMPLE 11, replace
# tmp_str = 'android:versionName="1.0.0.99"'
# print tmp_str.replace("1.0.0.99", "1.0.0.62")


# EXAMPLE 12, range
# for i in range(0,3):
#     print i
# 
# for i in xrange(0,3):
#     print i
# 
# def my_print(i):
#     print 'value %d' %i
# 
# [my_print(i) for i in xrange(0,3)]


# EXAMPLE 13, get time now
# from datetime import datetime
# now = datetime.now()
# print now


# EXAMPLE 14, copy file
# import os
# import shutil
# 
# path = r"D:\testDir"
# os.makedirs(path)
# 
# # shutil.copy(r"d:\release.keystore", path)
# # os.rename(r"D:\testDir\release.keystore", r"D:\testDir\rename.keystore")
# shutil.copyfile(r"D:\release.keystore", r"D:\testDir\rename.keystore")


# EXAMPLE 15, wait
# import subprocess
# 
# p = subprocess.Popen(r"ipconfig >> d:\ipconfig.txt", shell=True)
# p.wait()
#  
# p = subprocess.Popen(r"ipconfig >> d:\ipconfig.txt", shell=True)
# p.wait()


# EXAMPLE 16, tuple
# item = ("a","b","c")
# print item[2]


# EXAMPLE 17, RegEpx replace
# import re
# tmp_str_1 = "<meta-data android:name=\"channel_number\" android:value=\"9999\" />"
# print re.sub('\d{4}', '1234', tmp_str_1, count=1)
# 
# tmp_str_2 = 'versionname = "1.0.0.99", versioncode = "19"'
# print re.sub("[0-9]\.[0-9]\.[0-9]\.\d{2}", "1.0.0.64", tmp_str_2, count=1)


# EXAMPLE 18
# tmp_str = '09-09 13:04:21.364  1540  1815 W IntentResolver: resolveIntent: multiple matches, only some with CATEGORY_DEFAULT'
# print tmp_str[31]
# 
# keys = []
# for word in tmp_str.split(' '):
#     if word == 'W':
#         print word
#         keys.append(word)
#  
# print len(keys)


# EXAMPLE 19, RegExp
# import re
#  
# tmp_str = '01_test'
# if re.match(r'\d\d', tmp_str[0:2]):
#     print 'matched'
# else:
#     print 'mismatch'


# EXAMPLE 20, thread
# import threading
# import time
#  
# def exe_time():
#     print 'fn execution'
#     time.sleep(5)
#     print 'waited 5 seconds'
#  
# t = threading.Thread(target = exe_time)
# t.start()
# print 'start a new thread'
# t.join()


# EXAMPLE 21, subprocess
# # import os
# # output = os.popen('adb shell ps')
# 
# import subprocess
# p = subprocess.Popen('adb shell ps', shell=False, stdout=subprocess.PIPE)
# lines = p.stdout.readlines()
# 
# for line in lines:
#     if 'monkey' in line:
#         print line[10:].split(' ')[0]


# EXAMPLE 22, cal time
# import time
#  
# start = time.clock()
# time.sleep(2)
# end = time.clock()
# print 'time = %d millisec' %((end - start) * 1000)
# print 'time = %.3f seconds' %(end - start)
# print 'time = %d seconds' %(int(round(end - start)))


# EXAMPLE 23, index
# sub_str = 'tv.fun.settings/.general.GeneralSettingsActivity'
# tmp_str = 'mFocusedActivity: ActivityRecord{421f76b8 u0 tv.fun.settings/.general.GeneralSettingsActivity t17}'
# print tmp_str.index(sub_str)


# EXAMPLE 24, class
# class test(object):
#  
#     def __init__(self):
#         self.x = 'None'
#      
#     def set_x(self,x):
#         self.x = x
#          
#     def get_x(self):
#         return self.x
#  
# t = test()
# t.set_x('this is a test')
# print t.get_x()


# EXAMPLE 25, round
# print round(1.4)
# print round(1.5)
# print round(1.55)


# EXAMPLE 26, iterator
# tmp_arr = [('key1', 'value1', 'ex1'), ('key2', 'value2', 'ex2'), ('key3', 'value3', 'ex3')]
# key_arr = [k for (k,v,ex) in tmp_arr]
# print key_arr
#  
# val_arr = [v for (k,v,ex) in tmp_arr]
# print val_arr
# 
# ex_arr = [ex for (k,v,ex) in tmp_arr]
# print ex_arr


# EXAMPLE 27, dict iterator
# tmp_dict = {'key1':'value1', 'key2':'value2', 'key3':'value3'}
# for k in tmp_dict.keys():
#     print 'Key:', k
# 
# for v in tmp_dict.values():
#     print 'Value:', v
# 
# print tmp_dict.items()
# for (k, v) in tmp_dict.items():
#     print 'Key:', k
#     print 'Value:', v


# EXAMPLE 28, sub str
# tmp_str1 = '11'
# tmp_str2 = '12'
# print int(tmp_str1[1]) + int (tmp_str2[1])


# EXAMPLE 29, return multiple values
# def my_fn(x, y):
#     return 0, x + y
# 
# print my_fn(1, 3)


# EXAMPLE 30, build connection str
# params = {'server':'mpilgrim', 'database':'master', 'uid':'sa', 'pwd':'secret'}
# print ';'.join('%s=%s' % (k, v) for k, v in params.iteritems())


# EXAMPLE 31, print format str
# tmp_str = 'abcdefg'
# print '%.3s' % tmp_str
# 
# tmp_num = 10
# print 'Hex=%x, Dec=%d, Oct=%o' % (tmp_num, tmp_num, tmp_num)
# 
# import fpformat
# a = 0.0030000000005
# b = fpformat.fix(a, 6)
# print b
# 
# from decimal import Decimal
# x = '2.26'
# y = '2.29'
# c = Decimal(x) - Decimal(y)
# print c
# print round(c / Decimal(x) * 100, 2)


# EXAMPLE 32, time
# 1. get current time and format
# import time
# print time.time()
# print time.clock()
# print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
# 
# import datetime
# print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#  
# # 2. time compare
# t1 = time.strptime('2011-01-20 14:05', '%Y-%m-%d %H:%M')
# t2 = time.strptime('2011-01-20 16:05', '%Y-%m-%d %H:%M')
# print 't1 < t2:', t1 < t2
#  
# # 3. time delta
# print (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M')


# EXAMPLE 33, list to dict
# tmp_lst = ['Java', 'C#', 'C++', 'Python', 'JS']
# tmp_dict = dict.fromkeys(tmp_lst, 1)
# print 'Value:', tmp_dict
# print dir(tmp_dict)
# 
# tmp_key = 'Python'
# if tmp_key in tmp_dict:
#     print 'Found'
# print tmp_dict.has_key(tmp_key)


# EXAMPLE 34, list to generator
# tmp_lst = ['Java', 'C#', 'C++', 'Python', 'JS']
# tmp_gen = (v for v in tmp_lst)
# print 'Type:', type(tmp_gen)
# 
# for item in tmp_gen:
#     print 'item:', item


# EXAMPLE 35, closure
# passline = 60
# def my_func(val):
#     print 'address(val): %x' % id(val)
#     if val >= passline:
#         print 'pass'
#     else:
#         print 'failed'
#  
#     def in_func():
#         print val
#      
#     in_func()
#     return in_func
#  
# tmp_fn = my_func(89)
# tmp_fn()
# print tmp_fn.__closure__  # keep var "val"


# EXAMPLE 36, var context and closure
# 1
# def closure_without_default():
#     acts = []
#     for i in xrange(5):
#         acts.append(lambda x: x ** i)
#     return acts
# 
# acts = closure_without_default()
# print acts[0](2)
# print acts[1](2)
# print acts[2](2)
# 
# # 2
# def closure_with_default():
#     acts = []
#     for i in xrange(5):
#         acts.append(lambda x, i=i: x ** i)
#     return acts
# 
# acts2 = closure_with_default()
# print acts2[0](2)
# print acts2[1](2)
# print acts2[2](2)


# EXAMPLE 37, closure used as deco
# def dec(func):
#     print 'dec'
#       
#     def in_dec(*arg):
#         print 'in_dec'
#         if len(arg) == 0:
#             return 0
#         for val in arg:
#             if not isinstance(val, int):
#                 return 0
#   
#         return func(*arg)
#     # end in_dec
#     return in_dec
# # end dec
# 
# def my_sum(*arg):
#     print 'my_sum'
#     print 'Type:', type(arg), 'Value:', arg
#     return sum(arg)
# 
# # 1, call directly
# print my_sum(1, 2, 3)
# print '*' * 30
# 
# # 2, call with closure
# my_sum_result = dec(my_sum)
# print my_sum_result(1, 3, 4)
# print '*' * 30
# 
# @dec
# def my_average(*arg):
#     print 'my_average'
#     return sum(arg) / len(arg)
# 
# # 3, call with decorate
# print my_average(1, 3, 4)


if __name__ == '__main__':

    print os.path.basename(__file__), 'DONE!'
    pass
