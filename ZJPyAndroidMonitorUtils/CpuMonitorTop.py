# -*- coding: utf-8 -*-
'''
Created on 2016-6-16

@author: zhengjin

Parse and build CPU usage info by using top.

'''

import os
import time
from ZJPyAndroidMonitorUtils import MonitorUtils


# --------------------------------------------------------------
# Vars
# --------------------------------------------------------------
g_package_name = MonitorUtils.g_package_settings

g_run_num = '01'   # to be set
g_suffix = '%s_%s.txt' %(MonitorUtils.g_date, g_run_num)

g_report_dir_path = r'%s\top_cpu_log_%s' %(MonitorUtils.g_root_path, MonitorUtils.g_date)
g_report_file_path_top = r'%s\top_cpu_log_%s' %(g_report_dir_path, g_suffix)
g_report_file_path_top_package = r'%s\top_cpu_log_%s' %(g_report_dir_path, g_suffix)

g_run_time = 1 * MonitorUtils.g_min   # to be set
g_max_run_time = 60 * MonitorUtils.g_min
g_interval = MonitorUtils.g_long_interval   # seconds

g_flag_top = True
g_flag_top_for_package = False
g_flag_print_log = True  # to be set
g_flag_print_report = True


# --------------------------------------------------------------
# Functions: run commands
# --------------------------------------------------------------
def run_top_command():
    top_num = 3
    cmd = 'adb shell top -n 1 -m %s' %(top_num)
    if g_flag_print_log:
        print cmd

    lines = os.popen(cmd).readlines()
    return lines

def run_top_command_for_package():
    cmd_top = 'adb shell top -n 1'
    cmd_findstr = 'findstr -r "System tv.fun.filemanager"'
    cmd = '%s | %s' %(cmd_top, cmd_findstr)
    if g_flag_print_log:
        print cmd

    lines = os.popen(cmd).readlines()
    return lines

# --------------------------------------------------------------
# Functions: parse command output lines
# --------------------------------------------------------------
def build_header_for_top_cmd_output_line():
    cur_time = MonitorUtils.g_get_current_time()
    content = '%s -----------------------------------' %(cur_time)
    return content

# --------------------------------------------------------------
# Functions: create reports
# --------------------------------------------------------------
def build_report_header_for_top_cmd():
    header_title = '************** TOP CPU REPORT: %s' %(g_package_name)
    return header_title

def build_report_trailer_for_top_cmd():
    trailer_line = '************** TOP CPU REPORT, END'
    return trailer_line

def write_lines_report(f_report, lines):
    for line in lines:
        line = line.strip('\r\n')
        if line != '':
            if g_flag_print_report:
                print line
            f_report.write(line + MonitorUtils.g_new_line)

def write_line_report(f_report, line):
    line = line.strip('\r\n')
    if line != '':
        if g_flag_print_report:
            print line
        f_report.write(line + MonitorUtils.g_new_line)



# --------------------------------------------------------------
# Functions: parse reports
# --------------------------------------------------------------



# --------------------------------------------------------------
# Main
# --------------------------------------------------------------
def loop_process(fn, f_report):
    
    start = int(time.clock())
     
    while True:
        fn(f_report)
        time.sleep(g_interval)
 
        during = int(time.clock()) - start
        if during >= g_run_time or during >= g_max_run_time:
            print 'LOOP exit, and cost %d minutes %d seconds.' %((during/60), (during%60))
            break

def run_and_output_top_cmd_main(f_report):
    lines = run_top_command()

    write_line_report(f_report, build_header_for_top_cmd_output_line())
    write_lines_report(f_report, lines)
    f_report.flush()

def main():
    if g_flag_top:
        MonitorUtils.g_create_report_dir(g_report_dir_path)
        f_report = MonitorUtils.g_create_and_open_report_with_append(g_report_file_path_top)
        
        try:
            write_line_report(f_report, build_report_header_for_top_cmd())
            loop_process(run_and_output_top_cmd_main, f_report)
            write_line_report(f_report, build_report_trailer_for_top_cmd())
        finally:
            f_report.flush()
            f_report.close()


if __name__ == '__main__':
    main()
    print 'CPU monitor by top, DONE!'

    pass
