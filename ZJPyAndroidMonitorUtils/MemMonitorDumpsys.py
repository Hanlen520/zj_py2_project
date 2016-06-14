# -*- coding: utf-8 -*-
'''
Created on 2016-6-14

@author: zhengjin

'''

import os
from ZJPyAndroidMonitorUtils import MonitorUtils

# --------------------------------------------------------------
# Vars
# --------------------------------------------------------------
g_package_name = MonitorUtils.g_package_filemanager

g_flag_print_full_dumpsys_log = False
g_flag_print_log = True

# --------------------------------------------------------------
# Functions
# --------------------------------------------------------------
def run_dumpsys_meminfo_command():
    cmd = 'adb shell dumpsys meminfo %s' %(g_package_name)
    lines = os.popen(cmd)
    parse_report_line(lines)
    
def parse_report_line(lines):
    for line in lines:
        if g_flag_print_full_dumpsys_log:
            print line.strip('\n')

def parse_java_vm_heap_size(line):
    keyword = 'Dalvik Heap'
    if (keyword in line):
        words = line.split()
        heap_size = words[6]
        print heap_size
        heap_alloc = words[7]
        print heap_alloc

def parse_total_mem(line):
        keyword = 'TOTAL'
        if (keyword in line):
            words = line.split()
            print words[1]

def parse_activities_and_views(line):
    keyword = ' Views:'
    if (keyword in line):
        words = line.split()
        print words[1]

    keyword = ' Activities:'
    if (keyword in line):
        words = line.split()
        print words[3]

# --------------------------------------------------------------
# Main
# --------------------------------------------------------------
def mem_monitor_dumpsys_main():
    return True

if __name__ == '__main__':

    run_dumpsys_meminfo_command()
    print 'Memory monitor by dumpsys, DONE!'
    pass