# -*- coding: utf-8 -*-
'''
Created on 2016-6-17

@author: zhengjin
'''

import os
from ZJAndroidMonitor import MonitorUtils

# --------------------------------------------------------------
# Vars
# --------------------------------------------------------------
g_package_name = ''

g_flag_print_log = False


# --------------------------------------------------------------
# Functions: run commands
# --------------------------------------------------------------
def run_cmd_dumpsys_cpuinfo():
    cmd = 'adb shell dumpsys cpuinfo'
    if g_flag_print_log:
        print cmd

    lines = os.popen(cmd).readlines()
    return lines

def run_cmd_dumpsys_cpuinfo_for_package_and_total():
    cmd_dumpsys = 'adb shell dumpsys cpuinfo' 
    cmd_findstr = 'findstr -r "filemanager TOTAL"'
    cmd = '%s | %s' %(cmd_dumpsys, cmd_findstr)
    if g_flag_print_log:
        print cmd

    lines = os.popen(cmd).readlines()
    return lines


# --------------------------------------------------------------
# Functions: parse command output lines
# --------------------------------------------------------------
# TODO: 2016-6-17


# --------------------------------------------------------------
# Functions: create reports
# --------------------------------------------------------------
def print_output_lines(lines):
    for line in lines:
        print line.strip('\r\n')


# --------------------------------------------------------------
# Main
# --------------------------------------------------------------
def main():
    print_output_lines(run_cmd_dumpsys_cpuinfo())
#     print_output_lines(run_cmd_dumpsys_cpuinfo_for_package_and_total())


if __name__ == '__main__':
    
    g_package_name = MonitorUtils.g_pkg_name_filemanager
    
    main()

    print 'CPU monitor by dumpsys, DONE!'
