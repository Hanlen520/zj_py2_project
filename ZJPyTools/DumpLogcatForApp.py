# -*- coding: utf-8 -*-
'''
Created on 2017-7-27

@author: zhengjin
'''
import os
import time

from ZJPyUtils import RunCmds

# --------------------------------------------------------------
# Functions
# --------------------------------------------------------------
def dump_logcat_for_app_by_package(pkg_name, log_file_abs_path, timeout=10):
    import subprocess

    cmd_get_pids = 'ps | grep %s | busybox awk \'{print $2}\'' % pkg_name
    cmds = ['adb shell', cmd_get_pids, 'exit']
    ret_content = RunCmds.run_cmds_by_communicate(cmds)
    pids = get_pids_from_result(ret_content)
    
    filter_str = ''
    if len(pids) == 0:
        raise Exception('PID for package %s is not found!' % pkg_name)
    elif len(pids) == 1:
        filter_str = pids[0]
    else:
        filter_str = ' | '.join(pids)
    
    cmd_logcat = 'adb logcat -v time | findstr -r "%s" > %s' % (filter_str, log_file_abs_path)
    p = subprocess.Popen(cmd_logcat, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print 'dump log and wait %d seconds ...' % timeout
    time.sleep(timeout)
    p.kill()
    # stop adb

def get_pids_from_result(input_content):
    import re
    
    pids = []
    tmp_lines = input_content.replace('\r', '').split('\n')
    for line in tmp_lines:
        m = re.search(r'^[0-9]{4}', line)
        if m is not None:
            pids.append(m.group())
    return pids


# --------------------------------------------------------------
# Main
# --------------------------------------------------------------
if __name__ == '__main__':

    dump_logcat_for_app_by_package('tv.fun.settings', 'd:\log.test.txt')

    print os.path.basename(__file__), 'DONE!'
