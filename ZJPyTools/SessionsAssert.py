# -*- coding: utf-8 -*-
'''
Created on 2017/5/25
Invoke from scripts/CustomRules.js, which is Fiddler built-in script

@author: zhengjin
'''

import os
import time
import codecs
import sys, getopt

# --------------------------------------------------------------
# Sub functions
# --------------------------------------------------------------
def file_decode_with_unicode_escape(file_path):
    if not os.path.exists(file_path):
        raise IOError('File(%s) not found.' % file_path)

    with open(file_path, 'r') as f:
        lines = f.readlines()
    if len(lines) == 0:
        raise Exception('The file(%s) is empty.' % file_path)
    time.sleep(1)
    
    lines = [line.decode('unicode_escape') for line in lines]
    with codecs.open(file_path, 'w', 'utf-8') as f:
        f.writelines(lines)
        f.flush()

def filter_records_from_src_and_wirte_results(file_src, file_target, keyword):
    if not os.path.exists(file_src):
        raise IOError('File(%s) not found.' % file_src)

    with open(file_src, 'r') as f:
        lines = f.readlines()
    if len(lines) == 0:
        raise Exception('The file(%s) is empty.' % file_src)
    
    lines = [line.decode('unicode_escape') for line in lines if keyword in line]
    with codecs.open(file_target, 'a', 'utf-8') as f:
        f.writelines(lines)
        f.flush()


# --------------------------------------------------------------
# Main functions
# --------------------------------------------------------------
def usage():
    print '''
    Usage: sessions_assert.py [options...]
    Options:
    -f: file filter
    -d: file decode
    -h: help info
    Example: $python SessionsAssert.py -h
    $python SessionsAssert.py -d d:\\sessions_data.txt -f d:\\sessions_response.txt
    '''

def print_usage_and_exit(exit_code=0):
    usage()
    exit(exit_code)

def sessions_assert_main():
    time.sleep(1)

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hf:d:')
    except getopt.GetoptError, e:
        print 'Error:', e
        print_usage_and_exit(1)
    if len(opts) == 0:
        print_usage_and_exit(1)

    for opt, val in opts:
        if opt in ('-h', '--help'):
            print_usage_and_exit()
        elif opt == '-f':
            # val = abs_file_path_src
            filter_records_from_src_and_wirte_results(val, r'd:\session_assert_results.txt', 'retCode')
        elif opt == '-d':
            # val = abs_file_path_src
            file_decode_with_unicode_escape(val)
    exit(0)


if __name__ == '__main__':
    
    sessions_assert_main()
