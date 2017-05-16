# -*- coding: utf-8 -*-

import os

from PyDemo01 import run_ex_by_flag

# EXAMPLE 01, RegExp, findall
def ex01():
    import re

    # 1
    p = re.compile(r'\d+')
    print p.findall('one1two2three3four4')

    # 2
    re_link = '<a href="(.*)">(.*)</a>'
    tmp_link = '<a href="http://www.baidu.com">baidu</a>'
    cinfo = re.findall(re_link, tmp_link)

    for item in cinfo[0]:
        print item

run_ex_by_flag(ex01)


# EXAMPLE 02, decorate
def ex0201():
    def deco(func):
        def _deco():
            print 'before myfunc() called.'
            func()
            print '  after myfunc() called.'
        return _deco
       
    @deco
    def myfunc():
        print ' myfunc() called.'

    myfunc()

run_ex_by_flag(ex0201)

def ex0202():
    def jmilkfan(func):
        print 'func id: %x' % id(func)
         
        def in_jmilkfan(x, y):
            print 'call in_jmilkfan()'
            func(x, y)
         
        print 'call jmilkfan()'
        print 'in_jmilkfan(): %s' % in_jmilkfan.__closure__
        return in_jmilkfan
     
    @jmilkfan
    def chocolate(x, y):
        print 'chocolate(): %s' % chocolate.__closure__
        print 'call chocolate(), the value is: %d' % (x + y)
     
    chocolate(1, 2)

run_ex_by_flag(ex0202)


# EXAMPLE 03, encoded
def ex0301():
    # when read and compare Chinese word from txt file, 
    # convert the txt format to UTF-8 without BOM in Notepad++ first 
    str1 = "测试"
    str2 = "测试"
    print str1 == str2

run_ex_by_flag(ex0301)
  
def ex0302():
    f = open(r'd:\diff_output.txt', 'r')
    str1 = f.readline().strip('\n').strip()
    str2 = f.readline().strip()
    str3 = '测试'
    print 'str1--> %s str2--> %s str3 --> %s' % (str1, str2, str3)
    print 'str1--> %d str2--> %d str3 --> %d' % (len(str1), len(str2), len(str3))
      
    if (str2 == str3):
        print 'equal'
    else:
        print 'NOT equal'

run_ex_by_flag(ex0302)


# EXAMPLE 04, get mins and secs
def ex04():
    seconds = 200
    print '%d minutes, %d seconds' % (seconds / 60, seconds % 60)

run_ex_by_flag(ex04)


# EXAMPLE 05, print format datetime
def ex05():
    import time
    print time.strftime('%Y-%m-%d,%H:%M:%S')

run_ex_by_flag(ex05)


# EXAMPLE 06, find
def ex06():
    tmp_str = '16-03-15,18:01:19    RAM: 979M total, 145M free, 22M buffers, 295M cached, 3M shmem, 19M slab'
    if tmp_str.find('RAM', 20, 25):
        print 'found'
    else:
        print 'not found'

run_ex_by_flag(ex06)


# EXAMPLE 07, encode and decode
def ex07():
    print '*' * 20, 'encode cases.'
    u = u'中文'
    print u  # ok for both command line and eclipse console
    print u.encode('gbk')  # ok in cmd line with support gbk
    print u.encode('utf-8')  # ok in eclipse console with support utf-8
    print u.encode('utf-16')  # bad

    print '*' * 20, 'default decode cases.'
    tmp_str = '测试1'
    try:
        print tmp_str.encode('gbk')  # error, default decode is 'ascii'
    except Exception, e:
        print e
    print tmp_str.decode('utf-8').encode('gbk')  # manual set decode as 'utf-8'

    print '*' * 20, 'sys.setdefaultencoding() cases.'
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')  # set default decode as 'utf-8'

    tmp_str = '测试2'
    print tmp_str.encode('gbk')

run_ex_by_flag(ex07)


# EXAMPLE 08, system platform
def ex08():
    import sys
    print sys.platform

run_ex_by_flag(ex08)


# EXAMPLE 09, dir(), sum(), reduce()
def ex09():
    tmp_gen = (i for i in range(50) if i % 2)
    print '__iter__' in dir(tmp_gen)
    print 'next' in dir(tmp_gen)
    print type(tmp_gen)
    print sum(tmp_gen)
     
    tmp_list = [i for i in range(50) if i % 2]
    print type(tmp_list)
    print reduce(lambda x, y: x + y, tmp_list)

run_ex_by_flag(ex09)


# EXAMPLE 10, generator
def ex10():
    def add(item):
        return item + 1

    tmp_gen = (i for i in range(10) if i % 2)
    print type(tmp_gen)

    tmp_lst = map(add, tmp_gen)
    # tmp_gen_add = map(lambda x: x + 1, tmp_gen)
    print type(tmp_lst)
    for i in tmp_lst:
        print 'value %d' % i

run_ex_by_flag(ex10)


# EXAMPLE 11, RegExp basic
def ex11():
    import re

    s = 'afkak1aafal12345adadsfa'
    pattern = r'(\d)\w+(\d{2})'

    print '*' * 20, 'match case'
    m = re.match(pattern, s)
    if m is None:
        print 'null'
    else:
        print m

    print '*' * 20, 'search case'
    m = re.search(pattern, s)
    print m
    print m.group()
    print m.group(1, 2, 0)

    print '*' * 20, 'findall and split cases'
    print re.findall('(\W+)', 'words, words...')
    print re.split('\W+', '...words, words...')

    print re.split('[a-z]', '0A3b9z', flags=re.IGNORECASE)
    print re.split('[a-z]', '0A3b9z')

    print '*' * 20, 'match and search cases'
    m = re.search('(\w+) (\w+)', 'hello world zheng jin')
    print m.group()
    print m.group(1, 2, 0)
    print m.groups()

    print re.findall('(\w+) (\w+)', 'hello world zheng jin')

    print '*' * 20, 'match case'
    m = re.search('(..)+', 'a1b2c3')
    print m.group()

run_ex_by_flag(ex11)


# EXAMPLE 12, distinct
def ex12():
    tmp_tup = (1, 1, 3, 4, 4, 5, 6, 7, 6)
    print 'iterator 1:'
    for item in set(tmp_tup):
        print item

    print 'iterator 2:'
    tmp_list = [1, 1, 3, 4, 4, 5, 6, 7, 6]
    for item in set(tmp_list):
        print item

run_ex_by_flag(ex12)


# EXAMPLE 13, get input opts and args
def ex13():
    #!/usr/bin/env python
    # -*- coding: utf-8 -*-
    import sys, getopt

    def usage():
        print '''
        Usage: analyse_stock.py [options...]
        Options:
        -e : Exchange Name
        -c : User-Defined Category Name
        -f : Read stock info from file and save to db
        -d : delete from db by stock code
        -n : stock name
        -s : stock code
        -h : this help info
        >>> python test.py -s haha -n "HA Ha"
        '''

    def test_main():
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'he:c:f:d:n:s:')
            print 'input opts:', opts
            print 'input args:', args
        except getopt.GetoptError:
            usage()
            exit(1)
        if len(opts) == 0:
            usage()
            exit(1)

        print 'output:'
        for opt, val in opts:
            if opt in ('-h', '--help'):
                usage()
                exit(0)
            elif opt == '-d':
                print 'del stock %s' % val
            elif opt == '-f':
                print 'read file %s' % val
            elif opt == '-c':
                print 'user-defined %s' % val
            elif opt == '-e':
                print 'Exchange Name %s' % val
            elif opt == '-s':
                print 'Stock code %s' % val
            elif opt == '-n':
                print 'Stock name %s' % val
        # end for
        exit(0)
    # end test_main

    test_main()

run_ex_by_flag(ex13)


# EXAMPLE 14, update tuple and list
def ex14():
    tmp_tup = (1, 2, 3, 4)
    try:
        tmp_tup[2] = 20
    except Exception, e:
        print e
    print 'iterator 1:'
    for item in tmp_tup:
        print item
     
    tmp_list = [1, 2, 3, 4]
    tmp_list[1] = 20
    print 'iterator 2:'
    for item in tmp_list:
        print item

run_ex_by_flag(ex14)


# EXAMPLE 15, file writelines()
def ex15():
    lines = []
    lines.append("str1\n")
    lines.append("str2\n")
    lines.append("str3\n")
     
    f = None
    try:
        f = open(r'd:\test.txt', 'a')
        f.writelines(lines)
    finally:
        if f is not None:
            f.close()

run_ex_by_flag(ex15)


# EXAMPLE 16, list sort
def ex16():
    tmp_lst = []
    tmp_lst.append('16-06-15 16:13:33,total,979M total,43M free,23M buffers,342M cached,3M shmem,17M slab')
    tmp_lst.append('16-06-15 16:13:33,process,532M,43M,20M,18M,tv.fun.filemanager')
    tmp_lst.append('16-06-15 16:13:33,service,490M,18M,2M,1M,tv.fun.filemanager:remote')
    tmp_lst.append('16-06-15 16:13:38,process,532M,43M,20M,18M,tv.fun.filemanager')
    tmp_lst.append('16-06-15 16:13:40,total,979M total,43M free,23M buffers,342M cached,3M shmem,17M slab')

    tmp_lst_cp = tmp_lst[:]
    print '*' * 20, 'before sort'
    for item in tmp_lst_cp:
        print item

    list_upt = sorted(tmp_lst, key=lambda x:x.split(',')[1])
    print '*' * 20, 'after sorted'
    for item in list_upt:
        print item

    tmp_lst_cp.sort(key=lambda x:x.split(',')[1])
    print '*' * 20, 'after sort'
    for item in tmp_lst_cp:
        print item

run_ex_by_flag(ex16)


# EXAMPLE 17, sub string
def ex17():
    tmp_str = 'abcdefgh'
    print tmp_str[1:6]
    print tmp_str[0:]

run_ex_by_flag(ex17)


# EXAMPLE 18, *args
def ex18():
    def fun(title, *args):
        tmp_str = ', '.join([arg for arg in args])
        print title, tmp_str
      
    fun('program:', 'Java', 'JavaScript', 'Python')

run_ex_by_flag(ex18)


# EXAMPLE 19, empty list
def ex19():
    tmp_list = []
    print len(tmp_list)
    for item in tmp_list:
        print item

run_ex_by_flag(ex19)


# EXAMPLE 20, run shell cmd
def ex20():
    cmd = 'adb shell getprop | findstr heapgrowthlimit'
    lines = os.popen(cmd).readlines()

    if len(lines) == 1:
        print lines[0]
    else:
        print 'Error'
        for line in lines:
            print line

run_ex_by_flag(ex20)


# EXAMPLE 21, build in str functions
def ex21():
    print str.isalpha('a')
    print str.isalpha('1')

    print str.isdigit('a')
    print str.isdigit('1')

    print str.startswith('xyz', 'x')
    print str.endswith('xyz', 'z')

run_ex_by_flag(ex21)


# EXAMPLE 22, get file status
def ex22():
    import stat, time
    from fnmatch import fnmatch

    # 1: os.stat()
    print '*' * 20, 'os.stat()'
    def get_f_mode(f_status):
        if stat.S_ISDIR(f_status[stat.ST_MODE]): 
            return 'Directory'
        else:
            return 'File'

    f_path = r'E:\FX_me.txt'
    f_status = os.stat(f_path)
    f_info = {'Size': f_status[stat.ST_SIZE],
              'LastModified': time.ctime(f_status[stat.ST_MTIME]),
              'LastAccessed': time.ctime(f_status[stat.ST_ATIME]),
              'CreationTime': time.ctime(f_status[stat.ST_CTIME]),
              'Mode': get_f_mode(f_status)}

    for key, val in f_info.iteritems():
        print key + ': ' + str(val)

    # 2: os.path
    print '*' * 20, 'os.path()'
    if os.path.isdir(f_path):
        print 'directory'
    if os.path.isfile(f_path):
        print 'file'

    # 3: os.listdir()
    print '*' * 20, 'os.listdir()'
    f_items = os.listdir(os.getcwd())
    for f_name in f_items:
        if fnmatch(f_name, '*.py'):
            print f_name

run_ex_by_flag(ex22)


# EXAMPLE 23, os.walk()
def ex23():
    import fnmatch
    root_dir = os.getcwd()
     
    for root, folders, files in os.walk(root_dir):
        print 'folder count:', len(folders)
        print 'file count:', len(files)
        for file_name in files:
            if fnmatch.fnmatch(file_name, '*.py'):
                print os.path.join(root, file_name)

run_ex_by_flag(ex23)


# for unit test demo
def my_multiply(x, y):
    return x * y


if __name__ == '__main__':

    print '%s done!' % os.path.basename(__file__)
