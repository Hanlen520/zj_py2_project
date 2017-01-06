# -*- coding: utf-8 -*-
'''
Created on 2016-7-13

@author: zhengjin
'''

# EXAMPLE 01, platform
# import platform
# tmp_system = platform.system()
# print tmp_system
# if tmp_system == 'Windows':
#     print 'Win'
# else:
#     print 'Linux'
# 
# import sys
# print sys.platform


# EXAMPLE 02, os environ vars
# import os
# # if 'ANDROID_HOME' in os.environ:
# # if 'ANDROID_HOME' in os.environ.keys():
# if os.environ.has_key('ANDROID_HOME'):
#     print os.environ['ANDROID_HOME']


# EXAMPLE 03, get datetime
# import time
# print time.strftime('%Y-%m-%d %H:%M:%S')
# print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


# EXAMPLE 04, json loads and dumps
# import json
#    
# json_data = '{"data":{"name":"zhengjin", "age":30, "skill":["Java", "Python", "C++"]}, "retCode":"200"}'
# json_arr = json.loads(json_data, encoding='utf-8')
# print json_arr['retCode']
# print json_arr['data']['skill'][0]
#   
# json_obj = {'data': {'name': 'zhengjin', 'age': 30, 'skill': ['Java', 'Python', 'C++']}, 'retCode': '200'}
# json_str = json.dumps(json_obj, encoding='utf-8');
# print json_str
# print str(json_obj)


# EXAMPLE 05, encoded
# tmp_str = u'test'
# print type(tmp_str)
# print type(tmp_str.encode('utf-8'))


# EXAMPLE 06, send request
# import urllib2
# 
# url = 'http://apis.baidu.com/apistore/weatherservice/citylist?cityname=%E6%9C%9D%E9%98%B3'
# req = urllib2.Request(url)
# req.add_header("apikey", "11c756e31e9bed863a743ccff784ddeb")
# 
# resp = urllib2.urlopen(req)
# content = resp.read()
# if(content):
#     print(content)
# else:
#     print 'Error.'


# EXAMPLE 07, RegExp
# import re
#   
# tmp_str = '-28C'
# print re.findall(r'\d+', tmp_str)
# print re.findall(r'-?(\d+)C', tmp_str)


# EXAMPLE 08, dict
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


# EXAMPLE 09, sort
# tmp_dict = {'1':'a','3':'c','2':'b'}
# items = tmp_dict.items()
# items.sort()
# print items
# for k,v in items:
#     print k, v
#  
# for item in sorted(tmp_dict.items(), key=lambda x:x[0]):
#     print item


# EXAMPLE 10, +=
# i = 1
# i += 2
# print i


# EXAMPLE 11, encoded, decoded
# tmp_str_u = u'\u5317\u4eac'
# print type(tmp_str_u)
# print tmp_str_u
# print tmp_str_u.encode('utf-8')
# 
# tmp_str = '\u5317\u4eac'
# print type(tmp_str)
# print tmp_str.decode('unicode_escape')


# EXAMPLE 12, with block
# import os
# content = ''
# with open(os.path.join(os.getcwd(), 'zjunittest.log')) as f:
#     content = f.read()
# print content


# EXAMPLE 13, fn.__name__
# def my_print():
#     print 'it is a print test.'
#      
# def main(fn):
#     print 'exec function:', fn.__name__
#     fn()
# 
# main(my_print)


# EXAMPLE 14, RegExp
# import re
# str1 = '嫁个老公过日子（更新至24集）'
# str2 = '幸福满屋（全30集）'
# res = re.search('[至全](\d+)集',str2)
# print res.group(1)


# EXAMPLE 15, print last word
# tmp_str = 'test'
# print tmp_str[-1]


# EXAMPLE 16, os.popen()
# import os
# 
# cmd = 'ping 172.17.5.106'
# p = os.popen(cmd)
# print type(p)
# print len(p.readlines())


# EXAMPLE 17, global
# g_var = 'init'
# def print_var():
#     print 'Output:', g_var
#  
# print_var()


# EXAMPLE 18, class inherit
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


# EXAMPLE 19, run multiple cmds
# import subprocess
# print subprocess.call(["cmd"])
# 
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


# EXAMPLE 21, globals(), locals()
# var_global = 'test1'
# def my_print():
#     var_local = 'test2'
#     print var_local
#     print globals()  # print global vars can be access
#     print locals()  # print local vars can be access
#      
# my_print()


# EXAMPLE 22, stdout
# from sys import stdout 
# str1 = 'hello, zheng jin '
# str2 = 'it test.\n'
# stdout.write(str1)
# stdout.write(str2)


# EXAMPLE 23-1, sort
# def sortby(somelist, n):
#     nlist = [(x[n], x) for x in somelist]
# #     nlist.sort(key=lambda x:x[0], reverse=True)
#     nlist.sort()
#     return [val for (key, val) in nlist]
#    
# def sortby_inplace(somelist, n):
#     somelist[:] = [(x[n], x) for x in somelist]
#     somelist.sort()
#     somelist[:] = [val for (key, val) in somelist]
#    
# somelist = [(1, 2, 'def'), (2, -4, 'ghi'), (3, 6, 'abc')]
# somelist.sort()
# print somelist
#  
# # print sortby(somelist, 2)
# 
# sortby_inplace(somelist, 2)
# print somelist


# EXAMPLE 23-2, sort
# import operator
#  
# somelist = [(1, 2, 'def'), (2, -4, 'ghi'), (3, 6, 'abc')]
# somelist.sort(key=operator.itemgetter(2))
# print somelist


# EXAMPLE 24, iterator
# oldlist = ['test1', 'test2']
# newlist = []
# 
# # for word in oldlist:
# #     newlist.append(word.upper())
# # print newlist
# # 
# # newlist = [val.upper() for val in oldlist]
# # print newlist
# 
# newlist = map(str.upper, oldlist)
# print newlist


# EXAMPLE 25, iterator
# def my_upper(s):
#     return s.upper()
# 
# tmp_lst = ['hello', 'zhengjin']
# print [my_upper(val) for val in tmp_lst]
# print map(my_upper, tmp_lst)


# EXAMPLE 26, filter()
# def is_even(x):
#     return (x % 2) == 0
# 
# print range(10)
#  
# print [val for val in xrange(10) if is_even(val)]
# print filter(is_even, xrange(10))


# EXAMPLE 27, generate, yield
# def generate_ints(n):
#     for i in xrange(n):
#         yield i
#  
# gen = generate_ints(3)
# print gen.next()
# print gen.next()
# print next(gen)


# EXAMPLE 28, iterator
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


# EXAMPLE 29, *argv
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


# EXAMPLE 30, time format
# total_time = 45;
# print '%d h, %d mins' %(int(total_time / 60), int(total_time % 60))


if __name__ == '__main__':
    # EXAMPLE 17
#     g_var = 'update'
#     print_var()
    
    import os
    print '%s done!' %os.path.basename(__file__)
    pass
