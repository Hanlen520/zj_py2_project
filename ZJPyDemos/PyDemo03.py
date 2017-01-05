# -*- coding: utf-8 -*-

# EXAMPLE 01, RegExp, findall
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


# EXAMPLE 02, decorate
# def deco(func):
#     def _deco():
#         print 'before myfunc() called.'
#         func()
#         print '  after myfunc() called.'
#     return _deco
#  
# @deco
# def myfunc():
#     print ' myfunc() called.'
# 
# myfunc()
# myfunc()



# EXAMPLE 03, encoded
# when read and compare Chinese word from txt file, 
# convert the txt format to UTF-8 without BOM in Notepad++ first 
#
# str1 = "测试"
# str2 = "测试"
# print str1 == str2
 
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


# EXAMPLE 04, time format
# seconds = 200
# print '%d mins %d seconds' %(seconds / 60, seconds % 60)


# EXAMPLE 05, print format datetime
# import time
# print time.strftime('%y%m%d,%H:%M:%S')


# EXAMPLE 06, find
# tmp_str = '16-03-15,18:01:19    RAM: 979M total, 145M free, 22M buffers, 295M cached, 3M shmem, 19M slab'
# if tmp_str.find('RAM', 20, 25):
#     print 'found'
# else:
#     print 'not found'


# EXAMPLE 07, encoded
# u = u'中文'
# print u
# print u.encode('gb2312')
# print u.encode('utf-8')
# print u.encode('utf-16')


# EXAMPLE 08, platform
# import sys
# print sys.platform
# 
# from sys import platform
# print platform


# EXAMPLE 09, dir(), sum(), reduce()
# tmp_gen = (i for i in range(50) if i%2)
# # for attr in dir(tmp_gen):
# #     print attr
# print '__iter__' in dir(tmp_gen)
# print 'next' in dir(tmp_gen)
# print type(tmp_gen)
# print sum(tmp_gen)
# 
# tmp_list = [i for i in range(50) if i%2]
# print type(tmp_list)
# print reduce(lambda x, y: x + y, tmp_list)


# EXAMPLE 10, generator
# tmp_gen = (i for i in range(50) if i%2)
#  
# def add(item):
#     return (item + 1)
# tmp_gen_add = map(add, tmp_gen)
# # tmp_gen_add = map(lambda x: x + 1,tmp_gen)
# 
# print [i for i in tmp_gen_add]


# EXAMPLE 11, RegExp
# import re
  
# s = 'afkak1aafal12345adadsfa'
# pattern = r'(\d)\w+(\d{2})'
# m = re.match(pattern, s)
# if m is None:
#     print 'Null'
# else:
#     print m
# 
# m = re.search(pattern, s)
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


# EXAMPLE 12, distinct
# tmp_tup = [1, 1, 3, 4, 4, 5, 6, 7, 6]
# for item in set(tmp_tup):
#     print item
# 
# tmp_list = [1, 1, 3, 4, 4, 5, 6, 7, 6]
# for item in set(tmp_list):
#     print item


# EXAMPLE 13, get input opts and args
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
# 
# test_main()


# EXAMPLE 14, update tuple and list
# tmp_tup = (1,2,3,4)
# tmp_tup[2] = 20
# for item in tmp_tup:
#     print item
# 
# tmp_list = [1,2,3,4]
# tmp_list[1] = 20
# for item in tmp_list:
#     print item


# EXAMPLE 15, file writelines()
# lines = []
# lines.append("str1\n")
# lines.append("str2\n")
# lines.append("str3\n")
# 
# f = None
# try:
#     f = open(r'd:\test.txt', 'a')
#     f.writelines(lines)
# finally:
#     if f is not None:
#         f.close()


# EXAMPLE 16, list sort
# tmp_list = []
# tmp_list.append('16-06-15 16:13:33,total,979M total,43M free,23M buffers,342M cached,3M shmem,17M slab')
# tmp_list.append('16-06-15 16:13:33,process,532M,43M,20M,18M,tv.fun.filemanager')
# tmp_list.append('16-06-15 16:13:33,service,490M,18M,2M,1M,tv.fun.filemanager:remote')
# tmp_list.append('16-06-15 16:13:38,process,532M,43M,20M,18M,tv.fun.filemanager')
# tmp_list.append('16-06-15 16:13:40,total,979M total,43M free,23M buffers,342M cached,3M shmem,17M slab')
# 
# print '************** before sort'
# for item in tmp_list:
#     print item

# list_upt = sorted(tmp_list, key=lambda x:x.split(',')[1])
# print '************** after sort'
# for item in list_upt:
#     print item

# tmp_list.sort(key=lambda x:x.split(',')[1])
# print '************** after sort'
# for item in tmp_list:
#     print item


# EXAMPLE 17, sub string
# tmp_str = '012345'
# print tmp_str[0:6]
# print tmp_str[0:]


# EXAMPLE 18, *arg
# def fun(input_str, *arg):
#     print input_str
#      
#     for n in arg:
#         print n
#  
# fun('test', 'zheng', 'jin')


# EXAMPLE 19, empty list
# tmp_list = []
# print len(tmp_list)
# for item in tmp_list:
#     print item


# EXAMPLE 20, run shell cmd
# import os
# cmd = 'adb shell getprop | findstr heapgrowthlimit'
# lines = os.popen(cmd).readlines()
#  
# if len(lines) == 1:
#     print lines[0]
# else:
#     print 'Error'
#     for line in lines:
#         print line


# for unit test demo
def my_multiply(x, y):
    return x * y


if __name__ == '__main__':

    import os
    print '%s done!' %os.path.basename(__file__)
    pass
