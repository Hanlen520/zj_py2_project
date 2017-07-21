# -*- coding: utf-8 -*-
'''
Created on 2016-6-16

@author: zhengjin

Get CPU usage info by using top.
1) get the CPU info for top 10 process.
2) get the CPU info for package.
3) get the CPU info for package, and total CPU usage data.
'''

import os
import time
from ZJAndroidMonitor import MonitorUtils

# --------------------------------------------------------------
# Variables
# --------------------------------------------------------------
MAX_RUN_TIME = 8 * 60 * MonitorUtils.g_min  # 8 hours

g_suffix = ''
g_report_dir_path = ''
g_report_file_path_top_for_all = ''
g_report_file_path_top_for_pkg = ''
g_report_file_path_top_for_pkg_and_total = ''

def init_path_vars():
    global g_suffix
    global g_report_dir_path
    global g_report_file_path_top_for_all
    global g_report_file_path_top_for_pkg
    global g_report_file_path_top_for_pkg_and_total
    
    g_suffix = '%s_%s' % (MonitorUtils.g_cur_date, g_run_num)
    g_report_dir_path = r'%s\cpu_top_log_%s' % (MonitorUtils.g_root_path, g_suffix)
    g_report_file_path_top_for_all = r'%s\top_for_all_%s.txt' % (g_report_dir_path, g_suffix)
    g_report_file_path_top_for_pkg = r'%s\top_for_pkg_%s.txt' % (g_report_dir_path, g_suffix)
    g_report_file_path_top_for_pkg_and_total = r'%s\top_for_total_pkg_%s.txt' % (g_report_dir_path, g_suffix)


# --------------------------------------------------------------
# Functions: run commands
# --------------------------------------------------------------
def run_top_command():
    number_of_process = 10
    cmd = 'adb shell top -n 1 -m %s' % number_of_process
    ret_lines = os.popen(cmd).readlines()
    if len(ret_lines) == 0:
        print 'Run top command failed!'
        return 'null'
    return ret_lines

def run_top_command_for_pkg():
    cmd = 'adb shell top -n 1 | findstr ' + g_pkg_name
    ret_lines = os.popen(cmd).readlines()
    if len(ret_lines) != 1:
        print 'Process %s is not running!' % g_pkg_name
        return 'null'
    return ret_lines[0]

def run_top_command_for_total_and_pkg():
    cmd_top = 'adb shell top -n 1'
    cmd_findstr = 'findstr -r "System PID %s"' % g_pkg_name
    cmd = '%s | %s' % (cmd_top, cmd_findstr)

    ret_lines = os.popen(cmd).readlines()
    min_output_lines_num = 3
    if len(ret_lines) < min_output_lines_num:
        print 'Process %s is not running!' % g_pkg_name
        return 'null'
    return ret_lines


# --------------------------------------------------------------
# Functions: create reports, and IOs
# --------------------------------------------------------------
def build_prefix_line_for_top_cmd_output():
    cur_datetime = MonitorUtils.g_get_current_datetime()
    return '%s -----------------------------------' % cur_datetime

def run_top_cmd_and_write_output(f_report):
    write_single_line_report(f_report, build_prefix_line_for_top_cmd_output())
    write_multiple_lines_report(f_report, run_top_command())
    f_report.flush()

def run_top_cmd_for_pkg_and_write_output(f_report):
    write_line = '  '.join((MonitorUtils.g_get_current_time(), run_top_command_for_pkg()))
    write_single_line_report(f_report, write_line)
    f_report.flush()

def run_top_cmd_for_total_pkg_and_write_output(f_report):
    write_single_line_report(f_report, build_prefix_line_for_top_cmd_output())
    write_multiple_lines_report(f_report, run_top_command_for_total_and_pkg())
    f_report.flush()

def build_report_header_for_top_cmd():
    return '************** TOP CPU REPORT: START' 

def build_report_trailer_for_top_cmd():
    return '************** TOP CPU REPORT: END'

def build_report_header_for_top_cmd_for_pkg():
    return '************** TOP CPU REPORT FOR PACKAGE: %s' % g_pkg_name

def build_report_trailer_for_top_cmd_for_pkg():
    return '************** TOP CPU REPORT FOR PACKAGE: END'

def build_report_title_for_top_cmd_for_pkg():
    return 'TIME  PID PR CPU% S  #THR     VSS     RSS PCY UID      Name'

def write_multiple_lines_report(f_report, lines):
    if len(lines) == 0:
        return

    for line in lines:
        line = line.rstrip('\r\n')
        if len(line) > 0:
            print line
            f_report.write(line + MonitorUtils.g_new_line)

def write_single_line_report(f_report, line):
    if len(line) == 0:
        return
    line = line.rstrip('\r\n')
    print line
    f_report.write(line + MonitorUtils.g_new_line)

def file_flush_and_close(f):
    if f is not None:
        f.flush()
        f.close()


# --------------------------------------------------------------
# Main
# --------------------------------------------------------------
def loop_process(run_top_fn, f_report):
    start = int(time.clock())

    while 1:
        run_top_fn(f_report)
        time.sleep(g_interval)

        during = int(time.clock()) - start
        if during >= g_run_time or during >= MAX_RUN_TIME:
            print 'CPU monitor(top) exit, cost %d minutes %d seconds.' % (during / 60, during % 60)
            break
        print 'CPU monitor(top) is running, %d minutes %d seconds.' % (during / 60, during % 60)

def run_top_cmd_main():
    f_report = MonitorUtils.g_create_and_open_report_with_append(g_report_file_path_top_for_all)
    try:
        write_single_line_report(f_report, build_report_header_for_top_cmd())
        loop_process(run_top_cmd_and_write_output, f_report)
        write_single_line_report(f_report, build_report_trailer_for_top_cmd())
    finally:
        file_flush_and_close(f_report)

def run_top_cmd_for_pkg_main():
    f_report = MonitorUtils.g_create_and_open_report_with_append(g_report_file_path_top_for_pkg)
    try:
        write_single_line_report(f_report, build_report_header_for_top_cmd_for_pkg())
        write_single_line_report(f_report, build_report_title_for_top_cmd_for_pkg())
        loop_process(run_top_cmd_for_pkg_and_write_output, f_report)
        write_single_line_report(f_report, build_report_trailer_for_top_cmd_for_pkg())
    finally:
        file_flush_and_close(f_report)

def run_top_cmd_for_total_pkg_main():
    f_report = MonitorUtils.g_create_and_open_report_with_append(g_report_file_path_top_for_pkg_and_total)
    try:
        write_single_line_report(f_report, build_report_header_for_top_cmd_for_pkg())
        loop_process(run_top_cmd_for_total_pkg_and_write_output, f_report)
        write_single_line_report(f_report, build_report_trailer_for_top_cmd_for_pkg())
    finally:
        file_flush_and_close(f_report)

def cpu_monitor_top_setup():
    init_path_vars()
    MonitorUtils.g_create_report_dir(g_report_dir_path)

def cpu_monitor_top_main():
    cpu_monitor_top_setup()
  
    if g_is_top_for_pkg:
        run_top_cmd_for_pkg_main()
    else:
#         run_top_cmd_main()
        run_top_cmd_for_total_pkg_main()


if __name__ == '__main__':

    g_pkg_name = 'com.bestv.ott'
    g_run_num = '01'
    g_interval = MonitorUtils.g_interval
    g_run_time = 60 * MonitorUtils.g_min
    
    g_is_top_for_pkg = False

    cpu_monitor_top_main()

    print 'CPU monitor by top, DONE!'
