# -*- coding: utf-8 -*-
'''
Created on 2017/5/25

@author: zhengjin

Invoke from scripts/CustomRules.js (Fiddler built-in script).
1) filter
2) decode
'''

import os
import time
import codecs
import sys, getopt

# --------------------------------------------------------------
# Constants
# --------------------------------------------------------------
g_results_file_abs_path = r'd:\session_assert_results.txt'


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

def filter_records_from_src_and_wirte_results(file_src, if_exp, file_target=g_results_file_abs_path):
    if not os.path.exists(file_src):
        raise IOError('File(%s) not found.' % file_src)

    with open(file_src, 'r') as f:
        lines = f.readlines()
    if len(lines) == 0:
        raise Exception('The file(%s) is empty.' % file_src)
    
    lines = [line.decode('unicode_escape') for line in lines if if_exp(line)]
    with codecs.open(file_target, 'a', 'utf-8') as f:
        f.writelines(lines)
        f.flush()

def exp_if_contains_ret_code(line):
    if 'retCode' in line:
        return True
    return False

def reg_exp_if_contains_ad_keyword(line):
    import re
    pattern = 'k=[6,8]00329[7,8]|mcid=[7,8]070|a77943|header:'
    m = re.search(pattern, line)
    
    if m is not None and len(m.group()) > 0:
        return True
    return False


# --------------------------------------------------------------
# Main functions
# --------------------------------------------------------------
def usage():
    print '''
    Usage: sessions_assert.py [options...]
    Options:
    -d: file decode
    -f: file filter
    -t: test with ad keywords
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
        opts, args = getopt.getopt(sys.argv[1:], 'hd:f:t:')
    except getopt.GetoptError, e:
        print 'Error:', e
        print_usage_and_exit(1)
    if len(opts) == 0:
        print_usage_and_exit(1)

    for opt, val in opts:
        # val = src_file_abs_path
        if opt in ('-h', '--help'):
            print_usage_and_exit()
        elif opt == '-d':
            file_decode_with_unicode_escape(val)
        elif opt == '-f':
            filter_records_from_src_and_wirte_results(val, exp_if_contains_ret_code)
        elif opt == '-t':
            filter_records_from_src_and_wirte_results(val, reg_exp_if_contains_ad_keyword)
    exit(0)


if __name__ == '__main__':
    
    sessions_assert_main()

    print os.path.basename(__file__), 'DONE!'
