# -*- coding: utf-8 -*-
'''
Created on 2016-6-14

@author: zhengjin

Get the memory info for process by using dumpsys meminfo.

'''

import os
import time
from ZJAndroidMonitor import MonitorUtils
from ZJPyUtils import AdbUtils

# --------------------------------------------------------------
# Constants
# --------------------------------------------------------------
DEFAULT_NULL_CONTENT = 'null'
MAX_RUN_TIME = 12 * MonitorUtils.g_hour

WRITE_LINES = []
WRITE_LINES_BUF = 20


# --------------------------------------------------------------
# Path Variables
# --------------------------------------------------------------
g_report_dir_path = ''
g_report_file_path = ''

def init_path_vars(run_num):
    global g_suffix
    global g_report_dir_path
    global g_report_file_path

    g_suffix = '%s_%s' % (MonitorUtils.g_cur_date, run_num)
    g_report_dir_path = r'%s\mem_dumpsys_log_%s' % (MonitorUtils.g_root_path, g_suffix)
    g_report_file_path = r'%s\mem_dumpsys_log_%s.txt' % (g_report_dir_path, g_suffix)

def get_report_file_path_mem_dumpsys(run_num):
    init_path_vars(run_num)
    return g_report_file_path


# --------------------------------------------------------------
# Functions: run commands and parse output
# --------------------------------------------------------------
def run_getprop_cmd():
    cmd = 'adb shell getprop | findstr -r "heapstartsize heapgrowthlimit dalvik.vm.heapsize"'
    lines = os.popen(cmd).readlines()
    return lines

def get_app_mem_size_limit():
    lines = run_getprop_cmd()
    lines_num = 3
    if len(lines) == lines_num:
        return lines 
    else:
        print 'Warn, get system memory properties!'
        return DEFAULT_NULL_CONTENT

def parse_dumpsys_meminfo_and_write_report(f_report):
    output_lines = run_dumpsys_meminfo_command()
    parse_line = parse_report_line(output_lines)
    write_single_line_in_report(f_report, parse_line)

def run_dumpsys_meminfo_command():
    cmd_dumpsys = 'adb shell dumpsys meminfo %s' % g_pkg_name
    cmd_findstr = 'findstr -r \"Dalvik TOTAL Views: Activities:\"'
    cmd = '%s | %s' % (cmd_dumpsys, cmd_findstr)
    lines = os.popen(cmd).readlines()
    return lines

def parse_report_line(lines):
    java_vm_heap_size = DEFAULT_NULL_CONTENT
    java_vm_heap_alloc = DEFAULT_NULL_CONTENT
    total_mem = DEFAULT_NULL_CONTENT
    app_views = DEFAULT_NULL_CONTENT
    app_activities = DEFAULT_NULL_CONTENT

    for line in lines:
        if 'Dalvik Heap' in line:
            java_vm_heap_size, java_vm_heap_alloc = parse_java_vm_heap_size(line)
        elif 'TOTAL' in line:
            total_mem = parse_total_mem(line)
        elif ' Views:' in line:
            app_views = parse_app_views(line)
        elif 'Activities:' in line:
            app_activities = parse_app_activities(line)

    java_vm_heap_size = format_mem_size(java_vm_heap_size)
    java_vm_heap_alloc = format_mem_size(java_vm_heap_alloc)
    total_mem = format_mem_size(total_mem)
    cur_time = MonitorUtils.g_get_current_time()
    tmp_fields = (cur_time, total_mem, java_vm_heap_size, java_vm_heap_alloc, app_activities, app_views)
    return MonitorUtils.g_report_limiter.join(tmp_fields)

def parse_java_vm_heap_size(line):
    words = line.split()
    heap_size = words[6]
    heap_alloc = words[7]
    return str(heap_size), str(heap_alloc)

def parse_total_mem(line):
    words = line.split()
    return str(words[1])

def parse_app_views(line):
    words = line.split()
    return str(words[1])

def parse_app_activities(line):
    words = line.split()
    return str(words[3])

def format_mem_size(size):
    return '%sK' % size


# --------------------------------------------------------------
# Functions: create report
# --------------------------------------------------------------
DIV_LINE = '*' * 30

def prepare_report_file():
    MonitorUtils.g_create_report_dir(g_report_dir_path)
    f_report = MonitorUtils.g_create_and_open_report_with_append(g_report_file_path)
    return f_report

def create_report_header(f_report):
    header_title = DIV_LINE + ' DUMPSYS MEMINFO REPORT: %s' % (g_pkg_name)
    write_single_line_in_report(f_report, header_title)

    tmp_line = get_app_mem_size_limit()
    if tmp_line != DEFAULT_NULL_CONTENT:
        for line in tmp_line:
            write_single_line_in_report(f_report, '*' + line.strip('\r\n'))
    
    col0 = '*Time'
    col1 = 'MemTotal(Pss)'
    col2 = 'DalvikHeapSize'
    col3 = 'DalvikHeapAlloc'
    col4 = 'AppActivities'
    col5 = 'AppViews'
    header_cols_line = MonitorUtils.g_report_limiter.join((col0, col1, col2, col3, col4, col5))
    write_single_line_in_report(f_report, header_cols_line)

def create_report_trailer(f_report):
    trailer_line = DIV_LINE + ' DUMPSYS MEMINFO REPORT: END'
    write_single_line_in_report(f_report, trailer_line)

def write_single_line_in_report(f_report, write_line):
    print write_line
    WRITE_LINES.append(write_line + MonitorUtils.g_new_line)
    if (len(WRITE_LINES) > WRITE_LINES_BUF):
        force_write_lines_in_report(f_report)

def force_write_lines_in_report(f_report):
    f_report.writelines(WRITE_LINES)
    f_report.flush()  # force to write content into file
    del WRITE_LINES[:]


# --------------------------------------------------------------
# Main
# --------------------------------------------------------------
def loop_process(monitor_fn, f_report):
    start = int(time.clock())
    while 1:
        monitor_fn(f_report)
        time.sleep(g_monitor_interval)

        during = int(time.clock()) - start
        msg_cost_time = 'and cost %d minutes %d seconds.' % (during / 60, during % 60)
        if during > g_run_time or during > MAX_RUN_TIME:
            print 'Monitor(dumpsys meminfo) exit, ' + msg_cost_time
            return
        print 'Monitor(dumpsys meminfo) is running, ' + msg_cost_time

def mem_monitor_dumpsys_setup():
    if not AdbUtils.verify_adb_devices_connect():
        print 'No adb devices connected!'
        exit(1)
    init_path_vars(g_run_num)

def mem_monitor_dumpsys_main():
    mem_monitor_dumpsys_setup()
    
    f_report = prepare_report_file()
    try:
        create_report_header(f_report)
        loop_process(parse_dumpsys_meminfo_and_write_report, f_report)
        create_report_trailer(f_report)
    finally:
        force_write_lines_in_report(f_report)
        f_report.close()


if __name__ == '__main__':

    g_pkg_name = 'tv.ismar.daisy'
    g_run_num = '01'
    g_monitor_interval = MonitorUtils.g_interval
    g_run_time = 3 * MonitorUtils.g_min
    mem_monitor_dumpsys_main()

    print 'Memory monitor by dumpsys meminfo, DONE!'
