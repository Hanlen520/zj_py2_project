# -*- coding: utf-8 -*-

# EXAMPLE 1
# import re
# 
# p = re.compile(r'\d+')
# print p.findall('one1two2three3four4')
# 
# relink = '<a href="(.*)">(.*)</a>'
# info = '<a href="http://www.baidu.com">baidu</a>'
# cinfo = re.findall(relink, info)
# 
# for item in cinfo:
#     print item[0]
#     print item[1]


# EXAMPLE 2
# def deco(func):
#     def _deco():
#         print("before myfunc() called.")
#         func()
#         print("  after myfunc() called.")
#     return _deco
# 
# @deco
# def myfunc():
#     print(" myfunc() called.")


# EXAMPLE 3
#
# when read and compare Chinese word from txt file, 
# convert the txt format to UTF-8 without BOM in Notepad++ first 
#
# str1 = "测试"
# str2 = "测试"
# print str1 == str2
# 
# f = open(r'd:\diff_output.txt', 'r')
# str1 = f.readline().strip('\n').strip()
# str2 = f.readline().strip()
# str3 = '测试'
# print 'str1--> %s str2--> %s str3 --> %s' %(str1, str2, str3)
# print 'str1--> %d str2--> %d str3 --> %d' %(len(str1), len(str2), len(str3))
# 
# if (str2 == str3):
#     print 'equal'
# else:
#     print 'NOT equal'


# EXAMPLE 4
#
# seconds = 200
# print '%d mins %d seconds' %(seconds / 60, seconds % 60)


# EXAMPLE 5
#
# import time
# print time.strftime('%y%m%d,%H:%M:%S')


# EXAMPLE 6
#
# str = '16-03-15,18:01:19    RAM: 979M total, 145M free, 22M buffers, 295M cached, 3M shmem, 19M slab'
# if str.find('RAM', 20, 25):
#     print 'found'
# else:
#     print 'not found'


# EXAMPLE 7
#
# u = u'中文'
# print u
# print u.encode('gb2312')
# print u.encode('utf-8')
# print u.encode('utf-16')


# EXAMPLE 8
#
# import sys
# print sys.platform
# from sys import platform
# print platform


# EXAMPLE 9
#
# gen = (i for i in range(50) if i%2)
# print '__iter__' in dir(gen)
# print 'next' in dir(gen)
# 
# print [i for i in gen]
# print sum(gen)


# EXAMPLE 10
#
# gen = (i for i in range(50) if i%2)
# 
# def add(item):
#     return (item + 1)
# 
# gen2 = map(add, gen)
# print [i for i in gen2]


# EXAMPLE 11
#
# import re
#  
# s = 'afkak1aafal12345adadsfa'
# pattern = r'(\d)\w+(\d{2})\w'
# m = re.match(pattern,s)
# if m is None:
#     print 'Null'
# else:
#     print m
#
# m = re.search(pattern,s)
# print m
# print m.group()
# print m.group(1,2,0)

# print re.findall('(\W+)', 'words, words...')

# print re.split("[a-z]","0A3b9z", flags=re.IGNORECASE)
# print re.split("[a-z]","0A3b9z")

# print re.split('(\W+)', '...words, words...')

# m=re.match(r"(\w+) (\w+)","hello world zheng jin")
# m=re.search("(\w+) (\w+)","hello world zheng jin")
# print m.group()
# print m.group(1,2,0)
# print m.groups()

# print re.findall("(\w+) (\w+)","hello world zheng jin")

# m=re.match(r"(..)+","a1b2c3")
# print m.group(1)


# EXAMPLE 12
#
# val=9
# 
# def test(flag):
#     global val
#     if flag:  
#         val = 1
#     else: 
#         print 'test' 
#     return val
# 
# print test(0)


# EXAMPLE 13
#
# lst = [1, 1, 3, 4, 4, 5, 6, 7, 6]
# for item in set(lst):
#     print item


# EXAMPLE 14
#
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import sys,getopt
# 
# def usage():
#     print '''''
#     Usage: analyse_stock.py [options...]
#     Options:
#     -e : Exchange Name
#     -c : User-Defined Category Name
#     -f : Read stock info from file and save to db
#     -d : delete from db by stock code
#     -n : stock name
#     -s : stock code
#     -h : this help info
#     test.py -s haha -n "HA Ha"
#     ''' 
#  
# def test_main():
#     try:
#         opts, args = getopt.getopt(sys.argv[1:],'he:c:f:d:n:s:')
#     except getopt.GetoptError:
#         usage()
#         sys.exit()
#     if len(opts) == 0:
#         usage()
#         sys.exit()  
#      
#     for opt, arg in opts:
#         if opt in ('-h', '--help'):
#             usage()
#             sys.exit()
#         elif opt == '-d':
#             print "del stock %s" % arg
#         elif opt == '-f':
#             print "read file %s" % arg
#         elif opt == '-c':
#             print "user-defined %s " % arg
#         elif opt == '-e':
#             print "Exchange Name %s" % arg
#         elif opt == '-s':
#             print "Stock code %s" % arg
#         elif opt == '-n':
#             print "Stock name %s" % arg  
#      
#     sys.exit()


# EXAMPLE 15
#
# arr = (1,2,3,4)
# arr[2] = 20
# for item in arr:
#     print item
# 
# list = [1,2,3,4]
# list[1] = 20
# for item in list:
#     print item


# EXAMPLE 16
#
# import os
# import sys
# 
# def verify_adb_connection():
#     output = os.popen('adb get-serialno')
#     lines = output.readlines()
#     
#     if (len(lines) == 1):
#         if (lines[0] == 'unknown\n'):
#             print 'There is no adb connection.'
#             sys.exit(1)
#         else:
#             return
#     elif (len(lines) > 1):
#         print 'There are more than one adb connection.'
#         sys.exit(1)
#     else:
#         print 'unknown error, checking the adb connection.'
#         sys.exit(1)


# EXAMPLE 17
#
# def format_test_report():
#     f = open(r'e:\testre.txt', 'r')
#     test_case = ''
#     test_class = ''
#     test_cases = []
#     flag_num = True
#     test_number = ''
#     flag_time = True
#     test_time = ''
#     
#     try:
#         lines = f.readlines()
#         for line in lines:
#             if ('test=' in line):
#                 test_case = line.split(' ')[1].strip('\n')
#             if ('class=' in line):
#                 test_class = line.split(' ')[1].strip('\n')
#                 test_cases.append('%s::%s' %(test_class, test_case)) 
#                 continue
#             if flag_num and ('numtests=' in line):
#                 test_number = line.split(' ')[1].strip('\n')
#                 flag_num = False
#                 continue
#             if flag_time and ('Time:' in line):
#                 test_time = line.split(' ')[1].strip('\n')
#                 flag_time = False
#     finally:
#         f.close()
#     
#     print test_number
#     print test_time
#     for case in set(test_cases):
#         print case


# EXAMPLE 18
#
# lines = []
# lines.append("str1\n")
# lines.append("str2\n")
# lines.append("str3\n")
# 
# f = open(r'd:\test.txt', 'a')
# f.writelines(lines)
# f.close()


# EXAMPLE 19
#
# list = []
# list.append('16-06-15 16:13:33,total,979M total,43M free,23M buffers,342M cached,3M shmem,17M slab')
# list.append('16-06-15 16:13:33,process,532M,43M,20M,18M,tv.fun.filemanager')
# list.append('16-06-15 16:13:33,service,490M,18M,2M,1M,tv.fun.filemanager:remote')
# list.append('16-06-15 16:13:38,process,532M,43M,20M,18M,tv.fun.filemanager')
# list.append('16-06-15 16:13:40,total,979M total,43M free,23M buffers,342M cached,3M shmem,17M slab')
#  
# print '************** before sort'
# for item in list:
#     print item
#  
# list.sort(key=lambda x:x.split(',')[1])
#  
# print '************** after sort'
# for item in list:
#     print item


# EXAMPLE 20
# str = '012345'
# print str[0:6]


if __name__ == '__main__':

#     myfunc()
#     myfunc()

#     test_main()

#     verify_adb_connection()

#     format_test_report()

    print("%s done!" %__file__)
    pass