# -*- coding: utf-8 -*-
'''
Created on 2016-11-9

@author: zhengjin

Push local App to the android shell system directory.

'''

import os
import time
import subprocess

from ZJPyUtils import AdbUtils, WinSysUtils


# ----------------------------------------------------
# Constants
# ----------------------------------------------------
TARGET_APP_DIR_PATH = r'C:\Users\zhengjin\Desktop'
SHELL_TMP_DIR_PATH = '/data/local/tmp/'
SHELL_SYSTEM_APP_DIR_PATH = '/system/app/'


# ----------------------------------------------------
# Functions
# ----------------------------------------------------
def connect_to_device_with_root():
    if not AdbUtils.adb_connect_to_device(target_device_ip):
        print 'Failed adb connect to ' + target_device_ip
        exit(1)

    if not run_cmd_adb_root_from_subprocess_and_reconnect():
        print 'Failed adb root and reconnect to ' + target_device_ip
        exit(1)
        
def run_cmd_adb_root_from_subprocess_and_reconnect():
    cmd = 'adb root'
    print 'run adb root and reconnect.'
    p = subprocess.Popen(cmd, shell=True)
    time.sleep(1)
    p.kill()  # no return back for 'adb root' and kill instead
    
    return AdbUtils.adb_connect_to_device(target_device_ip)

def remount_system_partition():
    if not AdbUtils.adb_remount():
        print 'Failed to remount /system partition!'
        exit(1)

def push_app_to_shell_tmp_dir():
    print 'Start to push app to shell /data/local/tmp/'
    app_full_path = os.path.join(TARGET_APP_DIR_PATH, target_app_name)
    cmd = 'adb push %s %s' % (app_full_path, SHELL_TMP_DIR_PATH)
    
    if not WinSysUtils.run_sys_cmd(cmd):
        print 'Failed to push app to /data/local/tmp/ !'
        exit(1)

def check_app_push_to_shell_tmp_dir():
    cmd = 'adb shell ls %s | findstr %s' % (SHELL_TMP_DIR_PATH, target_app_name)
    output = WinSysUtils.run_sys_cmd_and_ret_content(cmd);
    
    if not target_app_name in output:
        print 'Check failed for push app to /data/local/tmp/ !'
        exit(1)

def copy_app_to_system_app_dir():
    print 'Copying app from sdcard to /system/app/'
    cmd = 'adb shell cp %s%s %s' % (SHELL_TMP_DIR_PATH, target_app_name, SHELL_SYSTEM_APP_DIR_PATH)
    if not WinSysUtils.run_sys_cmd(cmd):
        print 'Failed to copy app from sdcard to /system/app/'
        exit(1)

def remove_exit_apk_files_in_system_app_dir():
    file_pattern = '%s.*' % target_app_name.split('.')[0]
    cmd = 'adb shell rm ' + SHELL_SYSTEM_APP_DIR_PATH + file_pattern
    print cmd
    WinSysUtils.run_sys_cmd(cmd)
        
def check_app_copy_to_system_app_dir():
    cmd = 'adb shell ls %s | findstr %s' % (SHELL_SYSTEM_APP_DIR_PATH, target_app_name)
    output = WinSysUtils.run_sys_cmd_and_ret_content(cmd);
    
    if not target_app_name in output:
        print 'Check failed for copy app to /system/app'
        exit(1)

def change_mod_for_app_in_system():
    print 'Chmod for app to RO.'
    cmd = 'adb shell chmod 644 %s%s' % (SHELL_SYSTEM_APP_DIR_PATH, target_app_name)
    if not WinSysUtils.run_sys_cmd(cmd):
        print 'Failed to chmod for app in system!'
        exit(1)
    
def check_change_mod_for_app():
    cmd = 'adb shell ls -l %s | findstr %s' % (SHELL_SYSTEM_APP_DIR_PATH, target_app_name)
    output = WinSysUtils.run_sys_cmd_and_ret_content(cmd)
    
    read_only_auth = '-rw-r--r--'
    if not output.startswith(read_only_auth):
        print 'Check failed for chmod for app in system!'
        exit(1)


# ----------------------------------------------------
# Main
# ----------------------------------------------------
def main_push_app():
    connect_to_device_with_root()
    remount_system_partition()
    
    push_app_to_shell_tmp_dir()
    check_app_push_to_shell_tmp_dir()
    
    remove_exit_apk_files_in_system_app_dir()
    copy_app_to_system_app_dir()
    check_app_copy_to_system_app_dir()
    
    change_mod_for_app_in_system()
    check_change_mod_for_app()


if __name__ == '__main__':

    target_device_ip = '172.17.5.134'
    target_app_name = 'TVMediaPlayer.apk'

    main_push_app()
    
    print 'Push app to shell /system done!'
