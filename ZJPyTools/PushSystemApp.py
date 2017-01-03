# -*- coding: utf-8 -*-
'''
Created on 2016-11-9

@author: zhengjin

Push local App to the android /system/app

'''

import os

from ZJPyUtils import AdbUtils
from ZJPyUtils import WinSysUtils

# ----------------------------------------------------
# Variables
# ----------------------------------------------------
g_target_device_ip = ''
g_target_app_path = ''
g_target_app_name = ''

g_const_shell_sdcard_path = '/sdcard/'
g_const_shell_system_app_path = '/system/app/'
g_const_read_only_auth = '-rw-r--r--'


# ----------------------------------------------------
# Functions
# ----------------------------------------------------
def connect_to_device_with_root():
    if not AdbUtils.adb_connect_to_device(g_target_device_ip):
        print 'Failed adb connect to %s' %g_target_device_ip
        exit(1)
        
    if not AdbUtils.adb_connect_with_root(g_target_device_ip):
        print 'Failed adb root and connect to %s' %g_target_device_ip
        exit(1)
        
def remount_system_partition():
    if not AdbUtils.adb_remount():
        print 'Failed to remount /system partition!'
        exit(1)

def push_app_to_sdcard():
    print 'Start to push app to andorid sdcard.'
    app_full_path = os.path.join(g_target_app_path, g_target_app_name)
    cmd = 'adb push %s %s' %(app_full_path, g_const_shell_sdcard_path)
    
    if not WinSysUtils.run_sys_cmd(cmd):
        print 'Failed to push app to sdcard!'
        exit(1)

def check_app_push_to_sdcard():
    cmd = 'adb shell ls %s | findstr %s' %(g_const_shell_sdcard_path,g_target_app_name)
    output = WinSysUtils.run_sys_cmd_and_ret_content(cmd);
    
    if (not g_target_app_name in output):
        print 'Check failed for push app to sdcard!'
        exit(1)

def copy_app_from_sdcard_to_system_app():
    print 'Copying app from sdcard to /system/app'
    cmd = 'adb shell cp %s%s %s' %(g_const_shell_sdcard_path,g_target_app_name,g_const_shell_system_app_path)
    if (not WinSysUtils.run_sys_cmd(cmd)):
        print 'Failed to copy app from sdcard to /system/app'
        exit(1)
        
def check_app_copy_to_system_app():
    cmd = 'adb shell ls %s | findstr %s' %(g_const_shell_system_app_path,g_target_app_name)
    output = WinSysUtils.run_sys_cmd_and_ret_content(cmd);
    
    if (not g_target_app_name in output):
        print 'Check failed for copy app to /system/app'
        exit(1)

def change_mod_for_app_in_system():
    print 'Chmod for app to RO.'
    cmd = 'adb shell chmod 644 %s%s' %(g_const_shell_system_app_path,g_target_app_name)
    if (not WinSysUtils.run_sys_cmd(cmd)):
        print 'Failed to chmod for app in system!'
        exit(1)
    
def check_change_mod_for_app():
    cmd = 'adb shell ls -l %s | findstr %s' %(g_const_shell_system_app_path,g_target_app_name)
    output = WinSysUtils.run_sys_cmd_and_ret_content(cmd)
    
    if (not output.startswith(g_const_read_only_auth)):
        print 'Check failed for chmod for app in system!'
        exit(1)


# ----------------------------------------------------
# Main
# ----------------------------------------------------
def main_push_app():
    connect_to_device_with_root()
    remount_system_partition()
      
    push_app_to_sdcard()
    check_app_push_to_sdcard()
 
    copy_app_from_sdcard_to_system_app()
    check_app_copy_to_system_app()
     
    change_mod_for_app_in_system()
    check_change_mod_for_app()


if __name__ == '__main__':

    g_target_device_ip = '172.17.5.133'
    g_target_app_path = r'C:\Users\zhengjin\Desktop'
    g_target_app_name = 'TVWeather.apk'

    main_push_app()
    
    print 'Push app to android /system done!'
    pass
