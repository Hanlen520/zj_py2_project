# -*- coding: utf-8 -*-
'''
Created on 2016-6-14

@author: zhengjin

'''

import os
import time

from ZJPyAndroidMonitorUtils import MonitorUtils

# --------------------------------------------------------------
# Vars
# --------------------------------------------------------------
g_package_name = MonitorUtils.g_package_filemanager

g_run_num = '01'   # to be set
g_suffix = '%s_%s.txt' %(MonitorUtils.g_date, g_run_num)

g_report_dir_path = r'%s\dumpsys_mem_log_%s' %(MonitorUtils.g_root_path, MonitorUtils.g_date)
g_report_file_path = '%s\dumpsys_mem_log_%s' %(g_report_dir_path, g_suffix)

g_run_time = 3 * MonitorUtils.g_min   # to be set
g_max_run_time = 30 * MonitorUtils.g_min
g_interval = 5   # seconds

g_flag_print_log = False  # to be set
g_flag_print_report = True

g_write_lines = []
g_write_lines_buffer = 10


# --------------------------------------------------------------
# Parse Functions
# --------------------------------------------------------------
def dumpsys_meminfo_and_parse(f_report):
    output_lines = run_dumpsys_meminfo_command()
    parse_line = parse_report_line(output_lines)
    write_line_report(f_report, parse_line)

def run_dumpsys_meminfo_command():
    cmd_dumpsys = 'adb shell dumpsys meminfo %s' %(g_package_name)
    cmd_findstr = 'findstr -r \"Dalvik TOTAL Views: Activities:\"'
    cmd = '%s | %s' %(cmd_dumpsys, cmd_findstr)
    
    if g_flag_print_log:
        print 'log: %s' %(cmd)
    lines = os.popen(cmd)
    return lines
    
def parse_report_line(lines):
    java_vm_heap_size = ''
    java_vm_heap_alloc = ''
    total_mem = ''
    app_views = ''
    app_activities = ''
    
    for line in lines:
        if 'Heap' in line:
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
    cur_time = time.strftime(MonitorUtils.g_time_format)
    parse_line = (cur_time, total_mem, java_vm_heap_size, java_vm_heap_alloc, app_activities, app_views)

    return MonitorUtils.g_report_limiter.join(parse_line)

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
    return '%sK' %(size)


# --------------------------------------------------------------
# IO Functions
# --------------------------------------------------------------
def prepare_report_file():
    MonitorUtils.g_create_report_dir(g_report_dir_path)
    f_report = MonitorUtils.g_create_and_open_report_with_append(g_report_file_path)
    return f_report

def create_report_header(f_report):
    if g_flag_print_log:
        print 'log: create report header.'

    header_title = '************** DUMPSYS MEMINFO REPORT: %s' %(g_package_name)
    
    col0 = 'Time'
    col1 = 'MemTotal(Pss)'
    col2 = 'HeapSize'
    col3 = 'HeapAlloc'
    col4 = 'AppActivities'
    col5 = 'AppViews'
    header_col = MonitorUtils.g_report_limiter.join((col0, col1, col2, col3, col4, col5))
    
    write_line_report(f_report, header_title)
    write_line_report(f_report, header_col)

def create_report_trailer(f_report):
    if g_flag_print_log:
        print 'log: create report trailer.'

    trailer_line = '************** DUMPSYS MEMINFO REPORT END'
    write_line_report(f_report, trailer_line)

def write_line_report(f_report, line):
    if g_flag_print_report:
        print line

    line = line + MonitorUtils.g_new_line
    g_write_lines.append(line)
    
    if (len(g_write_lines) > g_write_lines_buffer):
        force_write_line_report(f_report)

def force_write_line_report(f_report):
    if g_flag_print_log:
        print 'force write line to the report file.'
    
    if len(g_write_lines) == 0:
        return
    
    f_report.writelines(g_write_lines)
    f_report.flush()   # force to write content into file
    del g_write_lines[:]


# --------------------------------------------------------------
# Loop functions
# --------------------------------------------------------------
def loop_process(fn, f_report):
    start = int(time.clock())
    
    while True:
        fn(f_report)
        time.sleep(g_interval)

        during = int(time.clock()) - start
        if during >= g_run_time or during >= g_max_run_time:
            print 'LOOP exit, and cost %d minutes %d seconds.' %((during / 60), (during % 60))
            break


# --------------------------------------------------------------
# Main
# --------------------------------------------------------------
def mem_monitor_dumpsys_main():
    f_report = prepare_report_file()
    
    try:
        create_report_header(f_report)
        loop_process(dumpsys_meminfo_and_parse, f_report)
    finally:
        create_report_trailer(f_report)
        force_write_line_report(f_report)
        f_report.close()


if __name__ == '__main__':
    mem_monitor_dumpsys_main()
    print 'Memory monitor by dumpsys, DONE!'
    
    pass