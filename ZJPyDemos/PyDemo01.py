# -*- coding: utf-8 -*-

'''
Created on 2014/9/24

@author: zhengjin
'''

# from __future__ import division

# EXAMPLE 1, struct
# import struct
# 
# print(struct.calcsize("P"))


# EXAMPLE 2, collection
# tmp_tup = ('t')
# print tmp_tup
# 
# tmp_arr = ['a']
# print tmp_arr[0]
# 
# tests = {'name':'henry'}
# tests['heigh'] = '173'
# print tests['heigh']


# EXAMPLE 3, file append
# f = open(r'd:\test.log', 'a')
# name1 = 'henry'
# name2 = 'vieira'
# f.write('test %s \n' %(name1))
# f.write('test %s' %(name2))
# 
# f.close()


# EXAMPLE 4, print float
# import math
# print '%.3f' %math.pi
# print '%.3f' %(5.0 / 4.0)


# EXAMPLE 5, split
# path = 'FramesLog_01_Baseline.log'
# print path.split('.')[0]


# EXAMPLE 6, join
# mylist = ['1','2','3','4','5']
# mysublist = []
# sublen = int(round(len(mylist) * 0.5))
# mysublist = mylist[0:sublen]
# 
# print mysublist
# print' : '.join(mylist)


# EXAMPLE 7, subprocess
# import subprocess
# p = subprocess.Popen("java -version", shell=True)


# EXAMPLE 8, os.path
# import os
# file_path = "e:\log.txt"
# if not os.path.exists(file_path):
#     print "The file (%s) is not found" %file_path


# EXAMPLE 9, if
# if (1==1) and (2==2):
#     print "success"


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
# tmp_str = '01_test';
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
# print round(1.4);
# print round(1.5);
# print round(1.55);


if __name__ == '__main__':

    import os
    print os.path.basename(__file__), 'DONE!'
    pass
