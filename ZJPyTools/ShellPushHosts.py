# -*- coding: utf-8 -*-
'''
Created on 2016-6-24

@author: zhengjin

Push and replace the hosts file on shell, for TV system upgrade in testing ENV.
'''

import os
import time
import subprocess

# ----------------------------------------------------
# Adb Functions
# ----------------------------------------------------
SHELL_HOSTS_PATH = '/system/etc/hosts'


# ----------------------------------------------------
# Adb Functions
# ----------------------------------------------------
def adb_connect_devices(device_ip):
    cmd = 'adb connect %s' % (device_ip)
    print cmd
    os.system(cmd)

def verify_device_connected():
    cmd = 'adb get-serialno'
    print cmd
    for line in os.popen(cmd).readlines():
        if 'unknown' in line:
            return False
    return True

def adb_root():
    cmd = 'adb root'
    print cmd
    p = subprocess.Popen(cmd, shell=True)
    time.sleep(1)
    p.kill()

def adb_remount():
    cmd = 'adb remount'
    print cmd
    lines = os.popen(cmd).readlines()
    for line in lines:
        if 'succeeded' in line:
            return
    print 'Error, adb remount failed.'
    exit(1)

def adb_push_file(src_win_path, target_shell_path):
    cmd = 'adb push %s %s' % (src_win_path, target_shell_path)
    print cmd
    os.system(cmd)

def connect_to_android_devices(device_ip):
    try_times = 3
    for i in range(0, try_times):
        print 'Try to connect to device %d times.' % (i + 1)
        adb_connect_devices(device_ip)
        if verify_device_connected():
            return
    
    print 'Error, adb connect to device failed.'
    exit(1)


# ----------------------------------------------------
# Main
# ----------------------------------------------------
def push_hosts_main():
    connect_to_android_devices(device_ip)
    adb_root()
    connect_to_android_devices(device_ip)
    adb_remount()
    adb_push_file(win_hosts_path, SHELL_HOSTS_PATH)


if __name__ == '__main__':

    device_ip = '172.17.5.134'
    win_hosts_path = r'E:\Project_TV\device_hosts\host_upgrade\hosts'
    push_hosts_main()

    print 'Replace hosts file done!'
