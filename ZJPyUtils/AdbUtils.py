# -*- coding: utf-8 -*-
'''
Created on 2016-7-20

@author: Vieira

Include the utils for adb and Shell env.

'''

import os
import time
import logging

from ZJPyUtils import WinSysUtils

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
    ret_content = WinSysUtils.run_sys_cmd_and_ret_content(cmd)
    if len(ret_content) == 0:
        return False
    if ('unknown' in ret_content) or ('error' in ret_content):
        return False
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
# adb external functions
# --------------------------------------------------------------
def adb_logcat_by_tag_and_ret_process(tag, file_path):
    cmd = 'adb logcat -c && adb logcat -s %s -v time -d > %s' % (tag, file_path)
    WinSysUtils.run_sys_cmd(cmd)

def open_app_details_settings(pkg_name):
    action = 'android.settings.APPLICATION_DETAILS_SETTINGS'
    cmd = 'adb shell am start -a "%s" -d "package:%s"' % (action, pkg_name)
    WinSysUtils.run_sys_cmd(cmd)


# --------------------------------------------------------------
# Main
# --------------------------------------------------------------
if __name__ == '__main__':

    print verify_adb_devices_serialno()
#     open_app_details_settings('tv.fun.settings')
#     dump_logcat_for_app_by_package('tv.fun.settings', 'd:\log.test.txt')

    print os.path.basename(__file__), 'DONE!'
