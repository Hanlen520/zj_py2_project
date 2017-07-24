# -*- coding: utf-8 -*-
'''
Created on 2016-7-20

@author: Vieira

Include the utils for adb and Shell env.

'''

import os
import time
import logging

from ZJPyUtils import WinSysUtils, RunCmds

# --------------------------------------------------------------
# adb functions
# --------------------------------------------------------------
def verify_adb_devices_connect():
    logging.debug('verify adb devices connected.')
    
    cmd = 'adb devices'
    if ':5555' in WinSysUtils.run_sys_cmd_and_ret_content(cmd):
        return True
    else:
        return False

def verify_adb_devices_serialno():
    logging.debug('verify adb devices connected.')
    
    cmd = 'adb get-serialno'
    if 'unknown' in WinSysUtils.run_sys_cmd_and_ret_content(cmd):
        return False
    else:
        return True

def adb_connect_to_device(device_ip):
    cmd = 'adb connect %s' % device_ip

    try_adb_connect_times = 3
    wait_time = 3
    for i in range(0, try_adb_connect_times):
        logging.debug('try to connect to adb device, %d times.' % (i + 1))
        WinSysUtils.run_sys_cmd(cmd)
        if verify_adb_devices_serialno():  # verify connect success
            return True
        time.sleep(wait_time)
    
    logging.error('Failed to connect to device!')
    return False

def adb_connect_with_root(device_ip):
    if not adb_connect_to_device(device_ip):  # adb connect
        return False
    if not adb_root():
        return False
    if not adb_connect_to_device(device_ip):  # adb connect as root
        logging.error('Failed to connect to device with root!')
        return False
    
    return True

def adb_root():
    output_lines = WinSysUtils.run_sys_cmd_in_subprocess('adb root')
    if (len(output_lines) == 0 or output_lines == ''):
        return True
    
    for line in output_lines:
        if 'already' in line:
            logging.debug('adbd is already running as root.')
            return True
        if 'adbd as root' in line:
            logging.debug('adb root success.')
            return True
    
    logging.error('Adb root failed!')
    for line in output_lines:
        logging.error(line)
    return False

def adb_remount():
    cmd = 'adb remount'
    output = WinSysUtils.run_sys_cmd_and_ret_content(cmd)
    if ('succeeded' in output):
        return True
    
    return False

def adb_stop():
    cmd = 'adb kill-server'
    WinSysUtils.run_sys_cmd(cmd)

# --------------------------------------------------------------
# adb logcat functions
# --------------------------------------------------------------
def adb_logcat_by_tag_and_ret_process(tag, file_path):
    cmd = 'adb logcat -c && adb logcat -s %s -v time -d > %s' % (tag, file_path)
    WinSysUtils.run_sys_cmd(cmd)

def open_app_details_settings(pkg_name):
    action = 'android.settings.APPLICATION_DETAILS_SETTINGS'
    cmd = 'adb shell am start -a "%s" -d "package:%s"' % (action, pkg_name)
    WinSysUtils.run_sys_cmd(cmd)

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

    open_app_details_settings('tv.fun.settings')
#     dump_logcat_for_app_by_package('tv.fun.settings', 'd:\log.test.txt')

    print '%s DONE!' % (os.path.basename(__file__))
