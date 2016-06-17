# -*- coding: utf-8 -*-
'''
Created on 2016-6-16

@author: zhengjin

Parse and build CPU usage info by using top.

'''

import os
from ZJPyAndroidMonitorUtils import MonitorUtils


# --------------------------------------------------------------
# Vars
# --------------------------------------------------------------
g_package_name = MonitorUtils.g_package_filemanager

g_flag_print_log = False


# --------------------------------------------------------------
# Functions: run commands
# --------------------------------------------------------------
def run_top_three_command():
    cmd = 'adb shell top -n 1 -m 3'
    if g_flag_print_log:
        print cmd

    lines = os.popen(cmd).readlines()
    return lines

def run_top_command_for_package():
    cmd = 'adb shell top -n 1 | findstr tv.fun.filemanager'
    if g_flag_print_log:
        print cmd

    lines = os.popen(cmd).readlines()
    return lines


# --------------------------------------------------------------
# Functions: parse command output lines
# --------------------------------------------------------------



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
    print_output_lines(run_top_three_command())
#     print_output_lines(run_top_command_for_package())


if __name__ == '__main__':
    main()
    print 'CPU monitor by top, DONE!'

    pass