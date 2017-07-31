# -*- coding: utf-8 -*-
'''
Created on 2017-7-27

@author: zhengjin

Dump logcat log for APP by process id.
'''
import os
import time
import re
import subprocess

from ZJPyUtils import RunCmds, AdbUtils

# --------------------------------------------------------------
# Constants
# --------------------------------------------------------------
WAIT_TIME_FOR_LOGCAT = 15  # seconds

PKG_NAME_LAUNCHER = 'com.bestv.ott'
PKG_NAME_FILEMANAGER = 'tv.fun.filemanager'


# --------------------------------------------------------------
# Functions
# --------------------------------------------------------------
def get_pids_filter_string(pkg_name):
    cmd_get_pids = 'ps | grep %s | busybox awk \'{print $2}\'' % pkg_name
    print cmd_get_pids
    cmds = ['adb shell', cmd_get_pids, 'exit']
    ret_content = RunCmds.run_cmds_by_communicate(cmds)
    pids = get_pids_from_results_content(ret_content)
    
    filter_str = ''
    if len(pids) == 0:
        print 'Error, PID for package (%s) is not found!' % pkg_name
        exit(1)
    elif len(pids) == 1:
        filter_str = pids[0]
    else:
        filter_str = ' | '.join(pids)
    return filter_str

def get_pids_from_results_content(input_content):
    tmp_lines = input_content.split('\r\n')
    pids = []
    for line in tmp_lines:
        if len(line.strip()) == 0:
            continue
        m = re.search(r'^[0-9]{4}', line)
        if m is not None:
            pids.append(m.group())

    return pids

def dump_logcat_by_process_id(filter_str, file_path):
    cmd_logcat = 'adb logcat -v time | findstr -r "%s" > %s' % (filter_str, file_path)
    print cmd_logcat
    p = subprocess.Popen(cmd_logcat, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    print 'Dump log and wait %d seconds ...' % WAIT_TIME_FOR_LOGCAT
    time.sleep(WAIT_TIME_FOR_LOGCAT)
    stop_logcat(p)

def stop_logcat(p):
    if p is not None:
        p.kill()
        time.sleep(1)
    AdbUtils.adb_stop()


# --------------------------------------------------------------
# Main
# --------------------------------------------------------------
def dump_logcat_for_app_main(pkg_name, file_path):
    if not AdbUtils.verify_adb_devices_connect():
        print 'Error, no adb devices connected!'
        exit(1)
    
    filter_str = get_pids_filter_string(pkg_name)
    dump_logcat_by_process_id(filter_str, file_path)


if __name__ == '__main__':

    pkg_name = PKG_NAME_FILEMANAGER
    file_path = os.path.join(os.getcwd(), 'logs', 'logcat_for_app_id.txt')
    
    dump_logcat_for_app_main(pkg_name, file_path)

    print os.path.basename(__file__), 'DONE!'
