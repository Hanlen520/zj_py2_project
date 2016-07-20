# -*- coding: utf-8 -*-

'''
Created on 2016-7-20

@author: Vieira
'''

import time
import logging

from ZJPyUtils import WinSysUtils


# --------------------------------------------------------------
# Adb shell functions
# --------------------------------------------------------------
def verify_adb_devices_connect():
    logging.debug('Verify there are adb devices connected.')
    
    cmd = 'adb devices'
    if ':5555' in WinSysUtils.run_sys_cmd_and_read(cmd):
        return True
    else:
        return False

def verify_adb_devices_serialno():
    logging.debug('Verify there are adb devices connected.')
    
    cmd = 'adb get-serialno'
    if 'unknown' in WinSysUtils.run_sys_cmd_and_read(cmd):
        return False
    else:
        return True

def try_to_adb_connect_to_device(target_ip):
    try_adb_connect_times = 3
    wait_time = 3

    for i in range(0,try_adb_connect_times):
        print 'try to connect to adb device, %d times.' %(i + 1)
        WinSysUtils.run_sys_cmd('adb connect %s' %target_ip)
        if verify_adb_devices_serialno():  # verify connect success
            return True
        time.sleep(wait_time)
    
    return False

def adb_connect_with_root():
    if not try_to_adb_connect_to_device():  # adb connect
        logging.error('Failed to connect to device!')
        return False
    if not adb_root():
        return False
    if not try_to_adb_connect_to_device():   # adb connect as root
        logging.error('Failed to connect to device with root!')
        return False
    
    return True

def adb_root():
    is_success,lines = WinSysUtils.run_sys_cmd_in_subprocess('adb root')
    if is_success:
        for line in lines:
            if 'already' in line:
                logging.info('adbd is already running as root.')
                return True
            elif 'adbd as root' in line:
                logging.info('adb root success.')
                return True
    
    logging.error('Adb root failed!')
    for line in lines:
        logging(line)
    return False


if __name__ == '__main__':

    pass
