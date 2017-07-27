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
from ZJPyUtils import AdbUtils

# --------------------------------------------------------------
# Variables
# --------------------------------------------------------------
g_suffix = ''
g_report_dir_path = ''
g_report_file_path_top_for_all = ''
g_report_file_path_top_for_pkg = ''
g_report_file_path_top_for_pkg_and_total = ''

def init_path_vars(run_num, root_path):
    global g_suffix
    global g_report_dir_path
    global g_report_file_path_top_for_all
    global g_report_file_path_top_for_pkg
    global g_report_file_path_top_for_pkg_and_total
    
    g_suffix = '%s_%s' % (MonitorUtils.g_get_current_date(), run_num)
    g_report_dir_path = r'%s\cpu_top_log_%s' % (root_path, g_suffix)
    g_report_file_path_top_for_all = r'%s\top_for_all_%s.txt' % (g_report_dir_path, g_suffix)
    g_report_file_path_top_for_pkg = r'%s\top_for_pkg_%s.txt' % (g_report_dir_path, g_suffix)
    g_report_file_path_top_for_pkg_and_total = r'%s\top_for_total_pkg_%s.txt' % (g_report_dir_path, g_suffix)

def get_report_file_path_top_for_pkg(run_num, root_path):
    # invoked from external
    init_path_vars(run_num, root_path)
    return g_report_file_path_top_for_pkg


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
DIV_LINE = '*' * 30

def build_report_header_title_line_for_top():
    if g_is_top_for_pkg:
        return DIV_LINE + ' TOP CPU REPORT FOR PACKAGE: START'
    else:
        return DIV_LINE + ' TOP CPU REPORT: START'

def build_report_header_info_line_for_top(pkg_name, interval):
    return '### package_name=%s monitor_interval=%s' % (pkg_name, interval)

def build_report_header_cols_line_for_top_pkg():
    return '*TIME  PID PR CPU% S  #THR     VSS     RSS PCY UID      Name'

def build_prefix_line_for_top_cmd_output():
    cur_datetime = MonitorUtils.g_get_current_datetime()
    return cur_datetime + ' ' + '-' * 40

def build_report_trailer_line_for_top():
    return DIV_LINE + ' TOP CPU REPORT: END'

def run_top_cmd_and_write_output(f_report):
    write_single_line_report(f_report, build_prefix_line_for_top_cmd_output())
    write_multiple_lines_report(f_report, run_top_command())
    f_report.flush()

def run_top_cmd_for_pkg_and_write_output(f_report):
    write_line = '%s   %s' % (MonitorUtils.g_get_current_time(), run_top_command_for_pkg())
    write_single_line_report(f_report, write_line)
    f_report.flush()

def run_top_cmd_for_total_pkg_and_write_output(f_report):
    write_single_line_report(f_report, build_prefix_line_for_top_cmd_output())
    write_multiple_lines_report(f_report, run_top_command_for_total_and_pkg())
    f_report.flush()

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
        time.sleep(g_monitor_interval)

        during = int(time.clock()) - start
        msg_run_time = '%d minutes %d seconds.' % (during / 60, during % 60)
        if during >= g_run_time or during >= MonitorUtils.g_max_run_time:
            print 'CPU monitor(top) exit, ' + msg_run_time
            return
        print 'CPU monitor(top) is running...' + msg_run_time

def run_top_cmd_main():
    f_report = MonitorUtils.g_create_and_open_report_with_append(g_report_file_path_top_for_all)
    try:
        title_line = build_report_header_title_line_for_top()
        info_line = build_report_header_info_line_for_top('All', g_monitor_interval)
        write_multiple_lines_report(f_report, (title_line, info_line))
        loop_process(run_top_cmd_and_write_output, f_report)
        write_single_line_report(f_report, build_report_trailer_line_for_top())
    finally:
        file_flush_and_close(f_report)

def run_top_cmd_for_pkg_main():
    f_report = MonitorUtils.g_create_and_open_report_with_append(g_report_file_path_top_for_pkg)
    try:
        title_line = build_report_header_title_line_for_top()
        info_line = build_report_header_info_line_for_top(g_pkg_name, g_monitor_interval)
        cols_line = build_report_header_cols_line_for_top_pkg()
        write_multiple_lines_report(f_report, (title_line, info_line, cols_line))
        loop_process(run_top_cmd_for_pkg_and_write_output, f_report)
        write_single_line_report(f_report, build_report_trailer_line_for_top())
    finally:
        file_flush_and_close(f_report)

def run_top_cmd_for_total_pkg_main():
    f_report = MonitorUtils.g_create_and_open_report_with_append(g_report_file_path_top_for_pkg_and_total)
    try:
        title_line = build_report_header_title_line_for_top()
        info_line = build_report_header_info_line_for_top(g_pkg_name, g_monitor_interval)
        write_multiple_lines_report(f_report, (title_line, info_line))
        loop_process(run_top_cmd_for_total_pkg_and_write_output, f_report)
        write_single_line_report(f_report, build_report_trailer_line_for_top())
    finally:
        file_flush_and_close(f_report)

def cpu_monitor_top_setup():
    if not AdbUtils.verify_adb_devices_connect():
        print 'Error, no adb devices connected!'
        exit(1)
    
    init_path_vars(g_run_num, g_report_root_path)
    MonitorUtils.g_create_report_dir(g_report_dir_path)

def cpu_monitor_top_main():
    cpu_monitor_top_setup()
    if g_is_top_for_pkg:
        run_top_cmd_for_pkg_main()
    else:
        run_top_cmd_main()
#         run_top_cmd_for_total_pkg_main()


if __name__ == '__main__':

    g_report_root_path = MonitorUtils.g_get_report_root_path()
    g_monitor_interval = MonitorUtils.g_short_interval

    g_pkg_name = MonitorUtils.g_pkg_name_launcher
    g_run_num = '01'
    g_run_time = 5 * MonitorUtils.g_min

    g_is_top_for_pkg = True

    cpu_monitor_top_main()

    print 'CPU monitor by top, DONE!'
