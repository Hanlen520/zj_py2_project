# -*- coding: utf-8 -*-

# EXAMPLE 01, compare
# num = 3
# if 2 < num < 4:
#     print "Chained comparison operators work! \n" * 3


# EXAMPLE 02, enumerate
# some_list = [(1, 2, 'def'), (2, -4, 'ghi'), (3, 6, 'abc')]
# tmp_list = [(val[2], idx, val) for (idx, val) in enumerate(some_list)]
# tmp_list.sort()
# print tmp_list
# 
# my_phrase = ["No", "one", "expects", "the", "Spanish", "Inquisition"]
# my_dict = {key : value for key, value in enumerate(my_phrase)}
# print my_dict


# EXAMPLE 03, subprocess, try catch block, help
# import subprocess
# from subprocess import CalledProcessError
# 
# try: 
#     output = subprocess.check_output('dir', shell=True)
#     print output
# except CalledProcessError, e:
#     print 'Return code', e.returncode
#     if len(e.output):
#         print 'Error message', e.output
# except Exception, e:
#     print e.message

# subprocess.Popen('dir', shell=True)

# help(subprocess)


# EXAMPLE 04, sort, lambda
# items = [5, 3, 4, 1]
# print sorted(items, cmp=lambda x,y : cmp(x, y))


# EXAMPLE 05, parse list for master scan
# lines = []
# try:
#     f = open(r'C:\Users\zhengjin\Desktop\app_file_observer_log')
#     lines = f.readlines()
# finally:
#     f.close()
#  
# items = []
# if len(lines) == 1:
#     items = lines[0].split(';')
# else:
#     exit()
#  
# for item in sorted(items, cmp=lambda x,y : cmp(x, y)):
#     print(item)
# end parse


# EXAMPLE 06, build item
# lines = []
# try:
#     f = open(r'C:\Users\zhengjin\Desktop\app_file_observer_log_format', 'r')
#     lines = f.readlines()
# finally:
#     f.close()
# 
# record = ''
# for line in lines:
#     record += line.strip('\n') + ';'
# print 'Output: ' + record
# 
# try:
#     f = open(r'C:\Users\zhengjin\Desktop\app_file_observer_log_new', 'w')
#     f.write(record)
# finally:
#     f.close()
# end build


# EXAMPLE 07, type, format
# print type('test')

# print '{0}.{1}'.format('demo', 'png')


# EXAMPLE 08, subprocess
# import subprocess
#  
# cmd = 'adb connect 172.16.13.158'
# p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE)
# p.wait()
# lines = p.stdout.readlines()
#  
# print 'Output: '
# for line in lines:
#     if 'already connected' in line:
#         print 'True'
#     else:
#         print 'False'


# EXAMPLE 09, subprocess, logcat
# import subprocess
# import time
# 
# cmd = r'adb logcat -v time *:i > d:\logcat.txt'
# p = subprocess.Popen(cmd, shell=False)
# print 'start logcat'
# 
# time.sleep(5)
# print 'wait for 5 sec'
#  
# cmd = r'taskkill /im adb.exe /f'
# p = subprocess.Popen(cmd, shell=False)
# p.wait()
# print 'adb process is killed'


# EXAMPLE 10, multiple lines of str
# cmd = 'monkey ' + \
#     '--pkg-whitelist-file /WhitePackageList.xml ' + \
#     '--throttle 500 ' + \
#     '--ignore-crashes --ignore-timeouts --ignore-native-crashes ' + \
#     '--pct-touch 0 --pct-motion 0 --pct-trackball 0 --pct-nav 50 --pct-majornav 30 --pct-syskeys 10 --pct-appswitch 10 --pct-flip 0 --pct-anyevent 0 ' + \
#     '-v -v -v ' + \
#     '1000000'
# 
# print 'Output: ' + cmd


# EXAMPLE 11, exec pipe commands
# import subprocess
#  
# p1 = subprocess.Popen('netstat -nao', stdout=subprocess.PIPE)
# p2 = subprocess.Popen('findstr 5037', stdin=p1.stdout, stdout=subprocess.PIPE)
# 
# # output 1
# # for line in p2.stdout.readlines():
# #     print line.rstrip();  # default: '\n','\r', '\t', ' '
# 
# # output 2
# out = p2.communicate()
# print out[0]


# EXAMPLE 12, system()
# import os
# ret_code = os.system('netstat -nao | findstr 5037')
# if ret_code == 0:
#     print 'pass'


# EXAMPLE 13, file path format
# import os
# import time
# 
# global_date = time.strftime("%Y%m%d")
# global_num = '01'
# global_mr_log_dir_for_win = r'D:\files_logs'
# suffix = 'png'
# file_path = os.path.join(global_mr_log_dir_for_win, ('mr_snapshot_%s_%s.%s' %(global_date, global_num, suffix)))
# print 'snapshot save %s' %(file_path)


# EXAMPLE 14, get current dir
# import sys
# print sys.path[0]
# 
# import os
# print os.getcwd()


# EXAMPLE 15, list files
# import os
# files = os.listdir(os.getcwd())
# for f in files:
#     if 'Demo' in f:
#         print f


# EXAMPLE 16
# exec the android actions for MAX times
#
# import os
# import time
# import subprocess
#  
# def exec_android_actions_right():
#     MAX_TIMES = 1200
#      
#     subprocess.Popen(r'adb logcat -c && adb logcat -v time > d:\log28.txt', shell=True)
#      
#     for i in range(0,MAX_TIMES):
#         os.system('adb shell input keyevent KEYCODE_DPAD_RIGHT')
#         print 'press right %d and wait 1 seconds.' %(i)
#         time.sleep(1)
# 
# exec_android_actions_right()


# EXAMPLE 17, index
# tmp_str = '1002540K total'
# print 'find position:', tmp_str.find('K')
# print 'index position:', tmp_str.index('K')


# EXAMPLE 18, global
# val = 9
# def test_global(flag):
#     global val
#     if flag:  # 0 = false
#         val = 1  
#     else:  
#         val = -1
#     return val
#  
# print test_global(0)
# print val


# EXAMPLE 19, file append
# path = r'd:\procrank_log.txt'
# f = open(path, 'a')
# f.write('testa' + '\n')
# f.write('test\ttest')
# f.close()


# EXAMPLE 20, file name
# path = r'd:\test.txt'
# f = None
# try:
#     f = open(path, 'r')
#     line = f.readline()
#     print line.strip()
#     print f.name
# finally:
#     if f is not None:
#         f.close()


# EXAMPLE 21, line format
# line1 = 'User 22%, System 19%, IOW 0%, IRQ 0%'
# line2 = 'User 22%, System 19%, IOW 0%, IRQ 0%'
# line3 = 'User 22%, System 19%, IOW 0%, IRQ 0%'
# lines = []
# lines.append(line1)
# lines.append(line2)
# lines.append(line3)
# 
# output_line = []
# output_lines = []
# output_lines.append('User,System,IOW,IRQ')
#     
# for line in lines:
#     cols = line.split(', ')
#     for col in cols:
#         temp_col = col.split(' ')[1]
#         output_line.append(temp_col)
#     temp_line = ','.join(output_line)
#     output_lines.append(temp_line)
#     del output_line[:]
#     
# for line in output_lines:
#     print line


# EXAMPLE 22, print
# str1 = 'test'
# str2 = 'zhengjin'
# print str1,str2


# EXAMPLE 23, os.path
# import os
# tmp_str = os.getcwd()
# print 'current dir path:', tmp_str
# print 'current dir name:', os.path.basename(tmp_str)
# print 'parent dir path:', os.path.dirname(tmp_str)


# EXAMPLE 24, dict as json
# json_obj = {'data': {'name': 'zhengjin', 'age': 30, 'title': 'tester', 'skills': ['Java','C++','Script']}, 
#             'retCode': 200}
# print json_obj['retCode']
# print json_obj['data']['name']
# for v in json_obj['data']['skills']:
#     print v
# 
# print str(json_obj)


if __name__ == '__main__':
    
    import os
    print os.path.basename(__file__), 'DONE!'
    pass
