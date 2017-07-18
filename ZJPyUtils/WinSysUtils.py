# -*- coding: utf-8 -*-

'''
Created on 2016-7-20

@author: Vieira

Include the utils on Windows env.

'''

import os
import time
import subprocess
import logging

# --------------------------------------------------------------
# Time functions
# --------------------------------------------------------------
def get_current_date_and_time():
    return time.strftime('%y-%m-%d_%H%M%S')

def get_current_date():
    return time.strftime('%Y%m%d')


# --------------------------------------------------------------
# Run system commands
# --------------------------------------------------------------
def run_sys_cmd(cmd):
    logging.debug('Run command: %s' % cmd)

    ret = os.system(cmd)
    if not ret == 0:
        logging.warn('Failed, run command %s, return code is %d' % (cmd, ret))
        return False
    return True

def run_sys_cmd_and_ret_lines(cmd):
    logging.debug('Run command: %s' % cmd)
    
    lines = os.popen(cmd).readlines()
    if len(lines) == 0:
        logging.warn('The output is null for command %s' % cmd)
    return lines

def run_sys_cmd_and_ret_content(cmd):
    logging.debug('Run command: %s' % cmd)

    content = os.popen(cmd).read()
    if content is None or content == '':
        logging.warn('The output is null for command %s' % cmd)
        content = ''

    return content

def run_sys_cmd_in_subprocess(cmd):
    logging.debug('Run command: %s' % cmd)

    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()

    lines_error = p.stderr.readlines()
    lines_output = p.stdout.readlines()
    if len(lines_error) > 0:
        return lines_error
    if len(lines_output) > 0:
        return lines_output
    logging.warn('The output is null for command %s' % cmd)
    return ''


# --------------------------------------------------------------
# Function profile
# --------------------------------------------------------------
def exec_fun_and_log_exec_time(fn, *argv):
    start = int(time.clock())
    if len(argv) == 0:
        fn()
    elif len(argv) == 1:
        fn(argv[0])
    elif len(argv) == 2:
        fn(argv[0], argv[1])
    else:
        logging.error('The number of arguments should be less or equal than 2.')

    during = int(time.clock()) - start
    cost_min = int(during / 60)
    cost_sec = int(during % 60)

    if len(argv) == 0:
        logging.info('Run [%s], cost %d minutes %d seconds.' % (fn.__name__, cost_min, cost_sec))
    else:
        logging.info('Run [%s] for params <%s>, cost %d minutes %d seconds.' 
                     % (fn.__name__, ','.join(argv), cost_min, cost_sec))

def exec_fun_with_ret_and_log_exec_time(fn, *argv):
    # TODO: 2016.11.17
    pass


# --------------------------------------------------------------
# Main
# --------------------------------------------------------------
if __name__ == '__main__':

    pass
