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
# Main
# --------------------------------------------------------------
def main():
    return


if __name__ == '__main__':

    print 'CPU monitor by top, DONE!'

    pass
