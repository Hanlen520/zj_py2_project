# -*- coding: utf-8 -*-

import os

from PyDemo01 import run_ex_by_flag

# EXAMPLE 01, compare
def ex01():
    tmp_num = 3
    if 2 < tmp_num < 4:
        print 'Chained comparison operators work! \n' * 3

run_ex_by_flag(ex01)


# EXAMPLE 02, enumerate
def ex02():
    some_list = [(1, 2, 'def'), (2, -4, 'ghi'), (3, 6, 'abc')]
    tmp_list = [(val[2], idx, val) for (idx, val) in enumerate(some_list)]
    tmp_list.sort()
    print tmp_list
     
    my_phrase = ['No', 'one', 'expects', 'the', 'Spanish', 'Inquisition']
    my_dict = {idx : value for idx, value in enumerate(my_phrase)}
    print my_dict

run_ex_by_flag(ex02)


# EXAMPLE 03, subprocess, try catch block, help
def ex03():
    import subprocess
    from subprocess import CalledProcessError
     
    cmd = 'java -version'
    # 1
    ret_code1 = subprocess.call(cmd, shell=True)
    if ret_code1 == 0:
        print 'run subprocess.call() success.'

    # 2    
    try: 
        ret_code2 = subprocess.check_call(cmd, shell=True)
        if ret_code2 == 0:
            print 'run subprocess.check_call() success.'
    except CalledProcessError, e:
        print 'Return code', e.returncode
        if len(e.output):
            print 'Error message', e.output
    except Exception, e:
        print e.message
       
    # 3
    try: 
        output = subprocess.check_output(cmd, shell=True)
        print output.decode('gbk')
        print 'run subprocess.check_output() success.'
    except CalledProcessError, e:
        print 'Return code', e.returncode
        if len(e.output):
            print 'Error message', e.output
    except Exception, e:
        print e.message

    # 4
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    p.wait()
    for line in p.stdout:
        print line.rstrip('\r\n').decode('gbk')
    print 'run subprocess.Popen() success.'

#     help(subprocess)

run_ex_by_flag(ex03)


# EXAMPLE 04, sorted, lambda
def ex04():
    tmp_items = [5, 3, 4, 1]
    print sorted(tmp_items, lambda x, y : cmp(x, y))
    print tmp_items

run_ex_by_flag(ex04)


# EXAMPLE 05, type, format
is_ex05_run = False
if is_ex05_run:
    print type('test')
    print '{0}.{1}'.format('test', 'png')


# EXAMPLE 06, subprocess
def ex06():
    import subprocess
      
    cmd = 'adb connect 172.17.5.79'
    p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE)
    p.wait()
    lines = p.stdout.readlines()
      
    for line in lines:
        if 'already connected' in line:
            print 'connected'
        else:
            print 'connecting ...'

run_ex_by_flag(ex06)


# EXAMPLE 07, subprocess
def ex07():
    import subprocess
    import time
     
    cmd = r'adb logcat -v time *:i > d:\logcat.test.txt'
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    print 'start logcat ...'
    
    print 'logging ...'
    time.sleep(5)
    p.terminate()

    cmd = r'taskkill /im adb.exe /f'
    ret_content = subprocess.check_output(cmd, shell=False)
    print ret_content.decode('gbk')
    print 'adb process is killed'

run_ex_by_flag(ex07)


# EXAMPLE 08, multiple lines of str
def ex08():
    tmp_cmd_str = 'monkey ' + \
        '--pkg-whitelist-file /WhitePackageList.xml ' + \
        '--throttle 500 ' + \
        '--ignore-crashes --ignore-timeouts --ignore-native-crashes ' + \
        '--pct-touch 0 --pct-motion 0 --pct-trackball 0 --pct-nav 50 --pct-majornav 30 --pct-syskeys 10 --pct-appswitch 10 --pct-flip 0 --pct-anyevent 0 ' + \
        '-v -v -v ' + \
        '1000000'
    print 'monkey command:', tmp_cmd_str
    
    tmp_cmd_lst = ['monkey', '--pkg-whitelist-file /WhitePackageList.xml', '--throttle 500',
            '--ignore-crashes --ignore-timeouts --ignore-native-crashes',
            '--pct-touch 0 --pct-motion 0 --pct-trackball 0 --pct-nav 50',
            '--pct-majornav 30 --pct-syskeys 10 --pct-appswitch 10 --pct-flip 0 --pct-anyevent 0',
            '-v -v -v', '1000000']
    print 'monkey command:', ' '.join(tmp_cmd_lst)

run_ex_by_flag(ex08)


# EXAMPLE 09, run piped commands
def ex09():
    import subprocess
      
    p1 = subprocess.Popen('netstat -nao', stdout=subprocess.PIPE)
    p2 = subprocess.Popen('findstr 5037', stdin=p1.stdout, stdout=subprocess.PIPE)
     
    # 1
    p2.wait()
    for line in p2.stdout.readlines():
        print line.rstrip()  # default: '\n','\r', '\t', ' '
     
    # 2
    p3 = subprocess.Popen('netstat -nao', stdout=subprocess.PIPE)
    p4 = subprocess.Popen('findstr 5037', stdin=p3.stdout, stdout=subprocess.PIPE)
    p4.wait()
    out = p3.communicate()
    print out[0]

run_ex_by_flag(ex09)


# EXAMPLE 10, os.system
def ex10():
    ret_code = os.system('netstat -nao | findstr 5037')
    if ret_code == 0:
        print 'pass'

run_ex_by_flag(ex10)


# EXAMPLE 11, get unique file name
def ex11():
    import time

    tmp_date = time.strftime('%Y%m%d')
    tmp_mr_log_dir_for_win = r'D:\files_logs'
    tmp_num = '01'
    suffix = 'png'
    file_path = os.path.join(tmp_mr_log_dir_for_win,
                             ('mr_snapshot_%s_%s.%s' % (tmp_date, tmp_num, suffix)))
    print 'snapshot save at: %s' % (file_path)

run_ex_by_flag(ex11)


# EXAMPLE 12, get current dir
def ex12():
    import sys
    print sys.path[0]

    print os.getcwd()

run_ex_by_flag(ex12)


# EXAMPLE 13, list files
def ex13():
    files = os.listdir(os.getcwd())
    for f in files:
        if f.endswith('.py'):
            print f

run_ex_by_flag(ex13)


# EXAMPLE 14, subprocess
def ex14():
    # exec android events for times
    import time
    import subprocess

    p = subprocess.Popen(r'adb logcat -c && adb logcat -v time > d:\log.test.txt', shell=True)

    MAX_TIMES = 10
    for i in range(0, MAX_TIMES):
        os.system('adb shell input keyevent KEYCODE_DPAD_RIGHT')
        print 'press right %d times, and wait 1 seconds.' % i
        time.sleep(0.5)
        
    p.kill()
    if os.system('adb kill-server') == 0:
        print 'adb is stopped.'

run_ex_by_flag(ex14)


# EXAMPLE 15, index
def ex15():
    tmp_str = '1002540K total'
    print 'find position:', tmp_str.find('K')
    print 'index position:', tmp_str.index('K')

run_ex_by_flag(ex15)


# EXAMPLE 16, global
G_VALUE = 9
def ex16():
    def test_global(test_flag):
        global G_VALUE
        # 1 = true, 0 = false
        if test_flag:
            G_VALUE = 1  
        else:  
            print 'test global var'

    test_global(1)
    print G_VALUE

run_ex_by_flag(ex16)


# EXAMPLE 17, file append
def ex17():
    f = open(r'd:\procrank_log.txt', 'a')
    f.write('testa' + '\n')
    f.write('test\ttest')
    f.close()

run_ex_by_flag(ex17)


# EXAMPLE 18, get file name
def ex18():
    f = None
    try:
        f = open(r'd:\log.test.txt', 'r')
        line = f.readline()
        print line.strip()
        print f.name
    finally:
        if f is not None:
            f.close()

run_ex_by_flag(ex18)


# EXAMPLE 19, line format
def ex19():
    line1 = 'User 22%, System 19%, IOW 0%, IRQ 0%'
    line2 = 'User 22%, System 19%, IOW 0%, IRQ 0%'
    line3 = 'User 22%, System 19%, IOW 0%, IRQ 0%'
    lines = []
    lines.append(line1)
    lines.append(line2)
    lines.append(line3)

    output_lines = []
    output_lines.append('User,System,IOW,IRQ')

    for line in lines:
        tmp_fields = line.split(', ')
        tmp_line = ','.join([field.split(' ')[1] for field in tmp_fields])
        output_lines.append(tmp_line)

    for line in output_lines:
        print line

run_ex_by_flag(ex19)


# EXAMPLE 20, os.path
def ex20():
    tmp_str = os.getcwd()
    print 'current dir path:', tmp_str
    print 'is abs path:', os.path.isabs(tmp_str)
    print 'parent dir path:', os.path.dirname(tmp_str)
    print 'current dir name:', os.path.basename(tmp_str)

run_ex_by_flag(ex20)


# EXAMPLE 21, dict as json
def ex21():
    json_obj = {'data': {'name': 'zhengjin', 'age': 30, 'title': 'tester', 'skills': ['Java', 'C++', 'Script']},
                'retCode': 200}
    print json_obj['retCode']
    print json_obj['data']['name']
    for v in json_obj['data']['skills']:
        print v
     
    # json to str
    print str(json_obj)
    
    import json
    # json object to json str
    print json.dumps(json_obj)

run_ex_by_flag(ex21)


# EXAMPLE 22, with as, class
def ex22():
    class controlledExecution(object):
        '''
        customized class used in with as block
        '''
         
        def __init__(self, value):
            self.my_value = value
             
        def __str__(self):
            return 'Value: %s' % self.my_value
         
        def __enter__(self):
            '''
            run when enter into with as block, 
            and return value to var
            '''
            if str.isdigit(self.my_value):
                print 'value is a number.'
            elif str.isalpha(self.my_value):
                print 'value is a char.'
            else:
                print 'invalid value!'
            return self
     
        def __exit__(self, type, value, traceback):
            '''
            run when exit from with as block, 
            and we can raise exception here
            '''
            if self.my_value == 'None':
                raise Exception('value is none!')
             
            print 'value set to default.'
            self.my_value = None
            return True
     
    input_val = 'None'
    try:
        with controlledExecution(input_val) as tmp_var:
    #         print tmp_var.__doc__
            print tmp_var
    except Exception, ex:
        print 'Error message:', ex.message

run_ex_by_flag(ex22)


# EXAMPLE 23, with as, class
def ex23():
    import time

    class MyTimer(object):

        def __init__(self, verbose=False, ignoreException=False):
            self.verbose = verbose
            self.ignoreException = ignoreException

        def __enter__(self):
            self.start = time.clock()
            return self

        def __exit__(self, *unused):
            if len(unused) > 0:
                print 'exception_type:', unused[0]
                print 'exception_value:', unused[1]
                print 'traceback:', unused[2]
             
            self.end = time.clock()
            self.secs = self.end - self.start
            self.msecs = self.secs * 1000

            if self.verbose:
                print 'elapsed time: %.2f ms' % round(self.msecs, 2)
            return self.ignoreException
    # end class

    def fib(n):
        if n in [1, 2]:
            return 1
        else:
            return fib(n - 1) + fib(n - 2)
    # end fib()
     
    # 1
    print '*' * 20, 'EXAMPLE 01'
    with MyTimer(True):
        print 'results', fib(30)

    # 2, raise exception
    print '*' * 20, 'EXAMPLE 02'
    try:
        with MyTimer(True, False):
            print 'results:', fib(30)
            raise Exception('ZjExTest')
    except Exception, e:
        print 'Exception (%s) was caught' % e
    else:
        print 'No Exception'
     
    # 3, ignore exception
    print '*' * 20, 'EXAMPLE 03'
    try:
        with MyTimer(True, True):
            print 'results:', fib(30)
            raise Exception('ZjExTest')
    except Exception, e:
        print 'Exception (%s) was caught' % e
    else:
        print 'No Exception'

run_ex_by_flag(ex23)


if __name__ == '__main__':
    
    print os.path.basename(__file__), 'DONE!'
