# -*- coding: utf-8 -*-
'''
Created on 2016-7-20

@author: Vieira

Include the utils for adb and Shell env.

'''

import time
import logging

from ZJPyUtils import WinSysUtils

# --------------------------------------------------------------
# Functions
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
    cmd = 'adb connect %s' %device_ip

    try_adb_connect_times = 3
    wait_time = 3
    for i in range(0,try_adb_connect_times):
        logging.debug('try to connect to adb device, %d times.' %(i+1))
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
    if not adb_connect_to_device(device_ip):   # adb connect as root
        logging.error('Failed to connect to device with root!')
        return False
    
    return True

def adb_root():
    output_lines = WinSysUtils.run_sys_cmd_in_subprocess('adb root')
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


# --------------------------------------------------------------
# Main
# --------------------------------------------------------------
if __name__ == '__main__':

    pass
