# -*- coding: utf-8 -*-

# EXAMPLE 1
# num = 3
# 
# if 2 < num < 4:
#     print("Chained comparison operators work! \n" * 3)



# EXAMPLE 2
# my_phrase = ["No", "one", "expects", "the", "Spanish", "Inquisition"]
# my_dict = {key : value for key, value in enumerate(my_phrase)}
# print my_dict


# EXAMPLE 3
# import subprocess

# output = subprocess.check_output('dir', shell=True)
# print(output)
# subprocess.Popen('dir', shell=True)
# help(subprocess)


# EXAMPLE 4
# items = ['b', 'a']
# print(sorted(items, cmp=lambda x,y : cmp(x, y)))


# EXAMPLE 5
# parse list for master scan
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


# EXAMPLE 6
# build item
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
# print('Output: ' + record)
# 
# try:
#     f = open(r'C:\Users\zhengjin\Desktop\app_file_observer_log_new', 'w')
#     f.write(record)
# finally:
#     f.close()
# end build


# EXAMPLE 7
# print type("hi")

# print '{0}.{1}'.format('demo', 'png')
 

# EXAMPLE 8
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


# EXAMPLE 9
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


# EXAMPLE 10
# multiple lines of str
# cmd = 'monkey ' + \
#     '--pkg-whitelist-file /WhitePackageList.xml ' + \
#     '--throttle 500 ' + \
#     '--ignore-crashes --ignore-timeouts --ignore-native-crashes ' + \
#     '--pct-touch 0 --pct-motion 0 --pct-trackball 0 --pct-nav 50 --pct-majornav 30 --pct-syskeys 10 --pct-appswitch 10 --pct-flip 0 --pct-anyevent 0 ' + \
#     '-v -v -v ' + \
#     '1000000'
# 
# print 'Output ' + cmd


# EXAMPLE 11
# exec multiple commands from subprocess
# import subprocess
# 
# p1 = subprocess.Popen('netstat -nao', stdout=subprocess.PIPE)
# p2 = subprocess.Popen('findstr 5037', stdin=p1.stdout, stdout=subprocess.PIPE)
# out = p2.communicate()
# 
# print out[0]


# EXAMPLE 12
# import subprocess
# import os
# 
# os.system('netstat -nao | findstr 5037')
#
# p = subprocess.Popen('', stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = False)
# p.stdin.write('')
# print p.stdout.read()

# os.system('adb shell')
# os.system('ls -l')

# p = subprocess.Popen(r'ipconfig', shell = False)
# out = p.communicate(r'/all')
# 
# print out


# EXAMPLE 13
# import os
# import time
# 
# global_date = time.strftime("%Y%m%d")
# global_num = '01'
# global_mr_log_dir_for_win = r'D:\files_logs'
# suffix = 'png'
# file_path = os.path.join(global_mr_log_dir_for_win, ('mr_snapshot_%s_%s.%s' %(global_date, global_num, suffix)))
# print 'snapshot save %s' %(file_path)


# EXAMPLE 14
# import sys
# print sys.path[0]

# import os
# print os.getcwd()


# EXAMPLE 15
# import os
# def read_tests_from_dir():
#     path = r'E:\Eclipse_Workspace\Python_Demo\Local_Package_01'
#     files = os.listdir(path)
#     for f in files:
#         if 'Demo' in f:
#             print os.path.join(path, f)


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


# EXAMPLE 17
# str = '1002540K total'
# index = str.find('K')
# print str[0:index]
# print str[(index):]


# EXAMPLE 18
# val = 9
# def test(flag):  
#     global val
#     if flag:  
#         val = 1  
#     else:  
#         print 'test'  
#     return val


# EXAMPLE 19
# path = r'd:\procrank_log.txt'
# f = open(path, 'a')
# f.write('testa' + '\n')
# f.write('test\ttest')
# f.close()


# EXAMPLE 20
# path = r'd:\test.txt'
# f = open(path, 'r')
# line = f.readline()
# print line
# print f.name
# f.close()


# EXAMPLE 21
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


# EXAMPLE 22
# str1 = 'test'
# str2 = 'zhengjin'
# print str1,str2




if __name__ == '__main__':
#     exec_android_actions_right()
#     print test(0)
    
    print("Demo done!")
    pass