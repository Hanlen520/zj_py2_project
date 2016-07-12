# -*- coding: utf-8 -*-

'''
Created on 2014/9/24

@author: zhengjin
'''

# from __future__ import division

# EXAMPLE 1
# import subprocess
# import struct

# comments
# print "hello world!"

# print(struct.calcsize("P"))


# EXAMPLE 2
# tests = {'name':'henry'}
# tests1 = ['a']
# print(tests1[0])
# tests['heig'] = '173'
# print(tests['heig'])


# EXAMPLE 3
# f = open(r'd:\test.log', 'a')
# name1 = 'henry'
# name2 = 'vieira'
# f.write('test %s \n' %(name1))
# f.write('test %s' %(name2))
# 
# f.close()


# EXAMPLE 4
# cal3 = 41411 / 57883
# 
# print('%.4f' %cal3)


# EXAMPLE 5
# path = 'FramesLog_01_Baseline.log'
# print(path.split('.')[0])


# EXAMPLE 6
# mylist = ['1','2','3','4','5']
# mysublist = []
# sublen = int(round(len(mylist) * 0.5))
# mysublist = mylist[0:sublen]
# print(mysublist)

# print(' : '.join(mylist))


# EXAMPLE 7
# import subprocess
# p = subprocess.Popen("java -version", shell=True)


# EXAMPLE 8
# import os
# filepath = "e:\log.txt"
# if(not os.path.exists(filepath)):
#     print("The file %s is not found" %filepath)
#     exit()


# EXAMPLE 9
# if ((1==1)
#     and (2==2)):
#     print("success")


# EXAMPLE 10
# import os
# version_num = "1.0.0.59"
# saved_apk_dir = os.path.join(r"E:\apk_build", version_num)
# print(saved_apk_dir)

# f = open(r"d:\logtest.txt", "w")
# f.write("hello world")
# f.close()


# EXAMPLE 11
# str = 'android:versionName="1.0.0.99"'
# print(str.replace("1.0.0.98", "1.0.0.62"))


# EXAMPLE 12
# for i in range(0,3):
#     print(i)


# EXAMPLE 13
# from datetime import datetime
# now = datetime.now()
# print(now)


# EXAMPLE 14
# import os
# import shutil
# path = r"D:\testDir"
#  
# os.makedirs(path)
# # shutil.copy(r"d:\release.keystore", path)
# # os.rename(r"D:\testDir\release.keystore", r"D:\testDir\rename.keystore")
# shutil.copyfile(r"D:\release.keystore", r"D:\testDir\rename.keystore")


# EXAMPLE 15
# p = subprocess.Popen(r"ipconfig >> d:\ipconfig.txt", shell=True)
# p.wait()
# 
# p = subprocess.Popen(r"ipconfig >> d:\ipconfig.txt", shell=True)
# p.wait()


# EXAMPLE 16
# item = ("a","b","c")
# print(item[2])


# EXAMPLE 17, regex
# import re
# str = "<meta-data android:name=\"channel_number\" android:value=\"9999\" />"
# print(re.sub('\d{4}', '1234', str, count=1))

# str = 'versionname = "1.0.0.99", versioncode = "19"'
# print(re.sub("[0-9]\.[0-9]\.[0-9]\.\d{2}", "1.0.0.64", str, count=1))

# zj_name = 'zhengjin'
# tmp_str = 'hello worlod %s' %(zj_name)
# print tmp_str


# EXAMPLE 18
# str = '09-09 13:04:21.364  1540  1815 W IntentResolver: resolveIntent: multiple matches, only some with CATEGORY_DEFAULT'
# print str[31]
# keys = []
# for word in str.split(' '):
#     if word == 'W':
#         print word
#         keys.append(word)
# 
# print len(keys)


# EXAMPLE 19
# import re
# 
# if re.match(r'\d\d', str[0:2]):
#     print 'true'
# else:
#     print 'false'


# EXAMPLE 20
# import threading
# import time
# 
# def exe_time():
#     time.sleep(5)
#     print 'waited 5 seconds'
# 
# t = threading.Thread(target = exe_time)
# t.start()
# print 'start a new thread'
# t.join()


# EXAMPLE 21
# import subprocess
# import os 
# 
# p = subprocess.Popen('adb shell ps', shell=False, stdout=subprocess.PIPE)
# # output = os.popen('adb shell ps')
# 
# lines = p.stdout.readlines()
# 
# for line in lines:
#     if 'monkey' in line:
#         print line[10:].split(' ')[0]


# EXAMPLE 22
# import time
# 
# start = time.clock()
# time.sleep(2)
# print 'time = %d' %(int(time.clock()) - int(start))


# EXAMPLE 23
# sub_str = 'tv.fun.settings/.general.GeneralSettingsActivity'
# str = 'mFocusedActivity: ActivityRecord{421f76b8 u0 tv.fun.settings/.general.GeneralSettingsActivity t17}'
# print str.index(sub_str)


# EXAMPLE 24
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


if __name__ == '__main__':

    print("Demo done!")
    pass