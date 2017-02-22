# -*- coding: utf-8 -*-
'''
Created on 2016-6-24

@author: zhengjin

Push and replace the hosts file on shell, for TV system upgrade in testing ENV.
'''

import os

# ----------------------------------------------------
# Adb Functions
# ----------------------------------------------------
def run_system_cmd(cmd):
    print cmd
    os.system(cmd)

def adb_connect_devices(g_device_ip):
    cmd = 'adb connect %s' %(g_device_ip)
    run_system_cmd(cmd)

def adb_root():
    cmd = 'adb root'
    run_system_cmd(cmd)

def adb_remount():
    cmd = 'adb remount'
    print cmd
    lines = os.popen(cmd).readlines()
    for line in lines:
        if 'succeeded' in line:
            return
        else:
            print 'Error, adb remount failed.'
            exit(1)

def adb_push_file(s_path,t_path):
    cmd = 'adb push %s %s' %(s_path,t_path)
    run_system_cmd(cmd)

def verify_device_connected():
    cmd = 'adb get-serialno'
    print cmd
    for line in os.popen(cmd).readlines():
        if 'unknown' in line:
            return False
    return True

def try_to_connect_to_devices(g_device_ip):
    try_times = 3
    for i in range(0,try_times):
        print 'Try to connect to device %d times.' %(i+1)
        adb_connect_devices(g_device_ip)
        if verify_device_connected():
            return
    
    print 'Error, adb connect to device failed.'
    exit(1)


# ----------------------------------------------------
# Main
# ----------------------------------------------------
def replace_hosts_main():
    g_device_ip = '172.17.5.101'
    try_to_connect_to_devices(g_device_ip)
    adb_root()
    try_to_connect_to_devices(g_device_ip)
    adb_remount()
    
    s_path = r'E:\Project_TV\device_hosts\host_upgrade\hosts'
    t_path = 'system/etc/hosts'
    adb_push_file(s_path, t_path)


if __name__ == '__main__':

    replace_hosts_main()

    print 'Replace hosts file done!'
    pass
