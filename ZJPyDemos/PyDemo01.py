# -*- coding: utf-8 -*-
'''
Created on 2014/9/24

@author: zhengjin
'''

import os
# from __future__ import division

def run_ex_by_flag(ex_fn, run_flag=False):
    if run_flag:
        ex_fn()

# EXAMPLE 01, struct
is_ex01_run = False
if is_ex01_run:
    import struct
    print(struct.calcsize('P'))


# EXAMPLE 02, collection
def ex02():
    tmp_tup = ('t')
    print tmp_tup

    tmp_arr = ['a', 'b']
    print tmp_arr[1]

    tmp_dic = {'name':'henry'}
    tmp_dic['heigh'] = '173'
    print tmp_dic

run_ex_by_flag(ex02)


# EXAMPLE 03, file append
def ex03():
    f = open(r'd:\test.log', 'a')
    name1 = 'henry'
    name2 = 'vieira'
    f.write('test %s \n' % name1)
    f.write('test ' + name2)
    f.close()

run_ex_by_flag(ex03)


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

run_ex_by_flag(ex06)


# EXAMPLE 07, subprocess
def ex07():
    import subprocess
    p = subprocess.Popen('java -version')
    p.wait()

run_ex_by_flag(ex07)


# EXAMPLE 08, os.path
def ex08():
    file_path = 'e:\log.txt'
    if not os.path.exists(file_path):
        print 'The file (%s) is not found!' % file_path

run_ex_by_flag(ex08)


# EXAMPLE 09, if
is_ex09_run = False
if is_ex09_run:
    if 1 == 1 and 2 == 2:
        print 'pass'


# EXAMPLE 10, file write
def ex10():
    version_num = '1.0.0.59'
    saved_apk_dir = os.path.join(r'E:\apk_build', version_num)
    print saved_apk_dir
    
    f = open(r'd:\logtest.txt', 'w')
    f.write("hello world")
    f.close()

run_ex_by_flag(ex10)


# EXAMPLE 11, replace
def ex11():
    tmp_str = 'android:versionName="1.0.0.99"'
    print tmp_str.replace('1.0.0.99', '1.0.0.62')

run_ex_by_flag(ex11)


# EXAMPLE 12, range, xrange
def ex12():
    for i in range(0, 3):
        print i
     
    for i in xrange(0, 3):
        print i
     
    def my_print(i):
        print 'value: %d' % i
     
    [my_print(i) for i in xrange(0, 3)]

run_ex_by_flag(ex12)


# EXAMPLE 13, get current date time
is_ex13_run = False
if is_ex13_run:
    from datetime import datetime
    tmp_now = datetime.now()
    print tmp_now


# EXAMPLE 14, copy file
def ex14():
    import shutil

    tmp_src_file = r'D:\debug.keystore'
    tmp_path = r'D:\testDir'
    
    if not os.path.exists(tmp_path):
        os.makedirs(tmp_path)
    shutil.copy(tmp_src_file, tmp_path)

    # os.rename(tmp_src_file, r'D:\testDir\rename.keystore')
    shutil.copyfile(tmp_src_file, os.path.join(tmp_path, 'rename.keystore'))

run_ex_by_flag(ex14)


# EXAMPLE 15, wait
def ex15():
    import subprocess
 
    p = subprocess.Popen(r"ipconfig >> d:\ipconfig.txt", shell=True)
    p.wait()
    p = subprocess.Popen(r"ipconfig >> d:\ipconfig.txt", shell=True)
    p.wait()

run_ex_by_flag(ex15)


# EXAMPLE 16, RegEpx replace
def ex16():
    import re
    tmp_str_1 = '<meta-data android:name="channel_number" android:value="9999" />'
    print re.sub('\d{4}', '1234', tmp_str_1, count=1)
     
    tmp_str_2 = 'versionname = "1.0.0.99", versioncode = "19"'
    print re.sub('[0-9]\.[0-9]\.[0-9]\.\d{2}', '1.0.0.64', tmp_str_2, count=1)

run_ex_by_flag(ex16)


# EXAMPLE 17
def ex17():
    tmp_str = '1540  1815 W IntentResolver: resolveIntent: multiple matches, only some with CATEGORY_DEFAULT'
    print tmp_str[31]
     
    keys = [word for word in tmp_str.split(' ') if word == 'W']
    if len(keys) > 0:
        print keys

run_ex_by_flag(ex17)


# EXAMPLE 18, RegExp
def ex18():
    import re
      
    tmp_str = '01_test'
    if re.match(r'\d\d', tmp_str[0:2]):
        print 'matched'
    else:
        print 'mismatch'

run_ex_by_flag(ex18)


# EXAMPLE 19, thread
def ex19():
    import threading
    import time
      
    def fn_wait():
        print 'sub fn execution, and waited 5 seconds ...\n'
        time.sleep(5)
      
    t = threading.Thread(target=fn_wait)
    t.start()
    print 'start a new thread ...'
    t.join()
    print 'thread demo done.'

run_ex_by_flag(ex19)


# EXAMPLE 20, subprocess
def ex20():
    import subprocess
    p = subprocess.Popen('adb shell ps', shell=False, stdout=subprocess.PIPE)
    lines = p.stdout.readlines()
     
    for line in lines:
        if 'monkey' in line:
            print line[10:].split(' ')[0]

run_ex_by_flag(ex20)


# EXAMPLE 21, print time
def ex21():
    import time
      
    start = time.clock()
    time.sleep(2)
    end = time.clock()
    print 'time = %d millisec' % ((end - start) * 1000)
    print 'time = %.3f seconds' % (end - start)
    print 'time = %d seconds' % (int(round(end - start)))

run_ex_by_flag(ex21)


# EXAMPLE 22, index
def ex22():
    sub_str = 'tv.fun.settings/.general.GeneralSettingsActivity'
    tmp_str = 'mFocusedActivity: ActivityRecord{421f76b8 u0 tv.fun.settings/.general.GeneralSettingsActivity t17}'
    print 'index at: %d' % tmp_str.index(sub_str)

run_ex_by_flag(ex22)


# EXAMPLE 23, class
class test(object):
  
    def __init__(self):
        self.x = 'None'
      
    def set_x(self, x):
        self.x = x
          
    def get_x(self):
        return self.x

def ex23():
    t = test()
    t.set_x('this is a test')
    print t.get_x()

run_ex_by_flag(ex23)


# EXAMPLE 24, round
is_ex24_run = False
if is_ex24_run:
    print round(1.4)
    print round(1.5)
    print round(1.55, 1)


# EXAMPLE 25, iterator
def ex25():
    def my_print(key, value, ext):
        print 'key: %s, value: %s, ext: %s' % (key, value, ext)
    
    tmp_arr = [('key1', 'value1', 'ex1'), ('key2', 'value2', 'ex2'), ('key3', 'value3', 'ex3')]
    [my_print(k, v, ex) for (k, v, ex) in tmp_arr]

run_ex_by_flag(ex25)


# EXAMPLE 26, dict iterator
def ex26():
    tmp_dict = {'key1':'value1', 'key2':'value2', 'key3':'value3'}
    for k in tmp_dict.keys():
        print 'key:', k
     
    for v in tmp_dict.values():
        print 'value:', v
     
    for (k, v) in tmp_dict.iteritems():
        print 'key: %s, value: %s' % (k, v)

run_ex_by_flag(ex26)


# EXAMPLE 27, sub str
def ex27():
    tmp_str1 = '11'
    tmp_str2 = '12'
    print int(tmp_str1[1]) + int(tmp_str2[1])

run_ex_by_flag(ex27)


# EXAMPLE 28, return multiple values
def ex28():
    def my_fn(x, y):
        return 0, x + y
    
    x, y = my_fn(1, 3)
    print 'x = %d, y = %d' % (x, y)

run_ex_by_flag(ex28)


# EXAMPLE 29, build url params
def ex29():
    tmp_params = {'server':'mpilgrim', 'database':'master', 'uid':'sa', 'pwd':'secret'}
    print ';'.join('%s=%s' % (k, v) for k, v in tmp_params.iteritems())

run_ex_by_flag(ex29)


# EXAMPLE 30, format number
def ex30():
    tmp_str = 'abcdefg'
    print '%.3s' % tmp_str
     
    tmp_num = 10
    print 'Hex=%x, Dec=%d, Oct=%o' % (tmp_num, tmp_num, tmp_num)
     
    import fpformat
    a = 0.0030000000005
    b = fpformat.fix(a, 6)
    print b
     
    from decimal import Decimal
    x = '2.26'
    y = '2.29'
    c = Decimal(x) - Decimal(y)
    print c
    print round(c / Decimal(x) * 100, 2)

run_ex_by_flag(ex30)


# EXAMPLE 31, datetime and time
def ex31():
    # 1. get current time and format
    import time
    print time.time()
    print time.clock()
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    import datetime
    print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 2. time compare
    t1 = time.strptime('2011-01-20 14:05', '%Y-%m-%d %H:%M')
    t2 = time.strptime('2011-01-20 16:05', '%Y-%m-%d %H:%M')
    print 't1 < t2:', t1 < t2

    # 3. time delta
    print (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M')

run_ex_by_flag(ex31)


# EXAMPLE 32, list to dict
def ex32():
    tmp_lst = ['Java', 'C#', 'C++', 'Python', 'JS']
    tmp_dict = dict.fromkeys(tmp_lst, 1)
    print 'dict:', tmp_dict
    print dir(tmp_dict)

    tmp_key = 'Python'
    if tmp_key in tmp_dict:
        print 'found:', tmp_key
    print 'has key:', tmp_dict.has_key(tmp_key)

run_ex_by_flag(ex32)


# EXAMPLE 33, list to generator
def ex33():
    tmp_lst = ['Java', 'C#', 'C++', 'Python', 'JS']
    tmp_gen = (v for v in tmp_lst)
    print 'Type:', type(tmp_gen)
     
    for item in tmp_gen:
        print 'item:', item

run_ex_by_flag(ex33)


# EXAMPLE 34, closure
def ex34():
    passline = 60
    def my_func(val):
        print 'address(val): %x' % id(val)
        if val >= passline:
            print 'pass'
        else:
            print 'failed'
      
        def in_func():
            print 'value:', val
          
        in_func()
        return in_func
      
    tmp_fn = my_func(89)
    tmp_fn()
    print tmp_fn.__closure__  # keep var 'val'

run_ex_by_flag(ex34)


# EXAMPLE 35, var context and closure
def ex35():
    # 1
    def closure_without_default():
        fns_act = []
        for i in xrange(5):
            fns_act.append(lambda x: x ** i)
        return fns_act

    fns_act = closure_without_default()
    print 'iterator 1:'
    for fn in fns_act:
        print fn(2)

    # 2
    def closure_with_default():
        fns_act = []
        for i in xrange(5):
            fns_act.append(lambda x, i=i: x ** i)
        return fns_act

    fns_act2 = closure_with_default()
    print 'iterator 2:'
    for fn in fns_act2:
        print fn(2)

run_ex_by_flag(ex35)


# EXAMPLE 36, closure used as deco
def ex36():
    def dec(func):
        print 'dec'
           
        def in_dec(*arg):
            print 'in_dec'
            if len(arg) == 0:
                return 0
            for val in arg:
                print val
                if not isinstance(val, int):
                    return 0
       
            return func(*arg)
        # end in_dec
        return in_dec
    # end dec
     
    def my_sum(*arg):
        print 'my_sum'
        print 'type:', type(arg), 'value:', arg
        return sum(arg)
     
    # 1, call directly
    print my_sum(1, 2, 3)
    print '*' * 30
     
    # 2, call with closure
    my_sum_result = dec(my_sum)
    print my_sum_result(1, 3, 4)
    print '*' * 30
     
    @dec
    def my_average(*arg):
        print 'my_average'
        return sum(arg) / len(arg)
     
    # 3, call with decorate
    print my_average(2, 3, 4)

run_ex_by_flag(ex36)


if __name__ == '__main__':

    print os.path.basename(__file__), 'DONE!'
