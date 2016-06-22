# -*- coding: utf-8 -*-
'''
Created on 2015-7-9

@author: zhengjin
'''

import os
import time
import MrBaseConstants

# ----------------------------------------------------
# adb utils
# ----------------------------------------------------
def restart_adb_with_root_auth(device_ip):
    cmd = 'adb root'
    print cmd
    output = os.popen(cmd)
    
    if 'already' in output.read():
        print 'adbd is already running as root'
        return
    
    for i in range(3):
        cmd = 'adb connect %s' %(device_ip)
        print cmd
        os.system(cmd)
        time.sleep(2)
        print 'try to connect %d times' %(i + 1)

        if verify_adb_devices_serialno():
            return
    
    print 'Error, when connect to the device with root!'
    exit()

def verify_adb_devices_serialno():
    cmd = 'adb get-serialno'
    print cmd
    
    output = os.popen(cmd)
    if 'unknown' in output.read():
        return False
    else:
        return True

def adb_disconnect_device():
    cmd = 'adb disconnect'
    print cmd
    os.system(cmd)

def adb_screen_capture():
    suffix = 'png'
    path = '%s_%s.%s' %(MrBaseConstants.capture_for_shell, time.strftime("%H%M%S"), suffix)
    cmd = 'adb shell screencap -p %s' %(path)
    print cmd
    os.system(cmd)

def adb_pull_logs_from_shell():
    cmd = 'adb pull %s %s' %(MrBaseConstants.mr_log_dir_for_shell, MrBaseConstants.mr_log_dir_for_win)
    print cmd
    os.system(cmd)

def mkdir_for_shell(path_dir):
    cmd = 'adb shell mkdir -p %s' %(path_dir)
    print cmd
    os.system(cmd)
    time.sleep(1)

def remove_dir_for_shell(path_dir):
    cmd = 'adb shell rm -rf %s' %(path_dir)
    print cmd
    os.system(cmd)
    time.sleep(1)

# ----------------------------------------------------
# logcat utils
# ----------------------------------------------------
def build_logcat_command():
    log_level = MrBaseConstants.log_level
    log_path = MrBaseConstants.mr_logcat_file_for_shell
    logcat_cmd = 'adb logcat -c && adb logcat -f {0} -v threadtime *:{1}'.format(log_path, log_level)

    return logcat_cmd

# ----------------------------------------------------
# utils
# ----------------------------------------------------
def create_log_dir_for_win(path_dir):
    if os.path.exists(path_dir):
        return
    else:
        os.mkdir(path_dir)
        time.sleep(1)
        print 'create directory %s on local' %(path_dir)


if __name__ == '__main__':

    pass