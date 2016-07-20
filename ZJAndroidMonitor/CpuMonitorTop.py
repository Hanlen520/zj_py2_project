# -*- coding: utf-8 -*-
'''
Created on 2016-6-16

@author: zhengjin

Parse and build CPU usage info by using top.

'''

import os
import time
from ZJAndroidMonitor import MonitorUtils

# --------------------------------------------------------------
# Env Vars
# --------------------------------------------------------------
g_package_name = ''

# default values
g_run_num = '01'
g_run_time = 5 * MonitorUtils.g_min
g_max_run_time = 60 * MonitorUtils.g_min
g_interval = MonitorUtils.g_long_interval

g_flag_top = False
g_flag_top_for_pkg = False
g_flag_parse_report_for_pkg = False

g_flag_print_log = False
g_flag_print_report = True


# --------------------------------------------------------------
# Path Vars
# --------------------------------------------------------------
g_suffix = '%s_%s' %(MonitorUtils.g_cur_date, g_run_num)
g_report_dir_path = ''
g_report_file_path_top = ''
g_report_file_path_top_for_pkg = ''
g_report_file_path_total_category = ''
g_report_file_path_pkg_category = ''

def init_path_vars():
    global g_report_dir_path
    global g_report_file_path_top
    global g_report_file_path_top_for_pkg
    global g_report_file_path_total_category
    global g_report_file_path_pkg_category
    
    g_report_dir_path = r'%s\top_cpu_log_%s' %(MonitorUtils.g_root_path, g_suffix)
    g_report_file_path_top = r'%s\top_cpu_log_%s.txt' %(g_report_dir_path, g_suffix)
    g_report_file_path_top_for_pkg = r'%s\top_for_package_cpu_log_%s.txt' %(g_report_dir_path, g_suffix)
    g_report_file_path_total_category = r'%s\top_cpu_log_for_total_category_%s.txt' %(g_report_dir_path, g_suffix)
    g_report_file_path_pkg_category = r'%s\top_cpu_log_for_pkg_category_%s.txt' %(g_report_dir_path, g_suffix)
    

# --------------------------------------------------------------
# Functions: run commands
# --------------------------------------------------------------
def run_top_command():
    top_num = 3
    cmd = 'adb shell top -n 1 -m %s' %(top_num)
    if g_flag_print_log:
        print cmd
    lines = os.popen(cmd).readlines()

    if len(lines) == 0:
        print 'Error, when run top command!'
        exit(1)
    return lines

def run_top_command_for_pkg():
    cmd_top = 'adb shell top -n 1'
    cmd_findstr = 'findstr -r "System PID %s"' %(g_package_name)
    cmd = '%s | %s' %(cmd_top, cmd_findstr)
    if g_flag_print_log:
        print cmd
    lines = os.popen(cmd).readlines()
    
    min_output_lines_num = 3
    if len(lines) < min_output_lines_num:
        print 'Error, when run top command for package!'
        exit(1)
    return lines

def build_prefix_for_top_cmd_output_line():
    cur_time = MonitorUtils.g_get_current_time()
    return '%s -----------------------------------' %(cur_time)

def run_top_cmd_and_write_output(f_report):
    write_single_line_report(f_report, build_prefix_for_top_cmd_output_line())
    write_multiple_lines_report(f_report, run_top_command())
    f_report.flush()

def run_top_cmd_for_pkg_and_write_output(f_report):
    write_single_line_report(f_report, build_prefix_for_top_cmd_output_line())
    write_multiple_lines_report(f_report, run_top_command_for_pkg())
    f_report.flush()


# --------------------------------------------------------------
# Functions: create reports, and IOs
# --------------------------------------------------------------
def build_report_header_for_top_cmd():
    return '************** TOP CPU REPORT: START' 

def build_report_trailer_for_top_cmd():
    return '************** TOP CPU REPORT: END'

def build_report_header_for_top_cmd_for_pkg():
    return '************** TOP CPU REPORT FOR PACKAGE: %s' %(g_package_name)

def build_report_trailer_for_top_cmd_for_pkg():
    return '************** TOP CPU REPORT FOR PACKAGE: END'

def write_multiple_lines_report(f_report, lines):
    for line in lines:
        line = line.strip('\r\n')
        if line != '':
            if g_flag_print_report:
                print line
            f_report.write(line + MonitorUtils.g_new_line)

def write_single_line_report(f_report, line):
    line = line.strip('\r\n')
    if line != '':
        if g_flag_print_report:
            print line
        f_report.write(line + MonitorUtils.g_new_line)

def read_lines_from_report(f_report):
    try:
        lines = f_report.readlines()
    finally:
        f_report.close()

    if len(lines) == 0:
        print 'There is no record in %s' %(f_report.name)
        exit(1)
    return lines

def file_close_and_flush(f):
    if f is not None:
        f.flush()
        f.close()


# --------------------------------------------------------------
# Functions: parse reports
# --------------------------------------------------------------
def parse_top_for_pkg_report(lines):
    lines_for_total = []
    lines_for_pkg = []
    flag_first_cols_line = True
    
    keyword_total = 'User'
    keywrod_cols = 'PID'
    for line in lines:
        if line.startswith(keyword_total):
            lines_for_total.append(line)
        elif flag_first_cols_line and (keywrod_cols in line):
            lines_for_pkg.append(line)
            flag_first_cols_line = False
        elif g_package_name in line:
            lines_for_pkg.append(line)

    return lines_for_total, lines_for_pkg

def parse_lines_for_total(lines):
    tmp_single_line = []
    tmp_lines = []
    tmp_lines.append('User,System,IOW,IRQ')
    
    for line in lines:
        cols = line.split(', ')
        for col in cols:
            tmp_single_line.append(col.split(' ')[1])
        tmp_lines.append(','.join(tmp_single_line))
        del tmp_single_line[:]
    
    return tmp_lines


# --------------------------------------------------------------
# Main
# --------------------------------------------------------------
def loop_process(fn, f_report):
    start = int(time.clock())
     
    while True:
        fn(f_report)
        time.sleep(g_interval)
        if g_flag_print_log:
            print 'CPU monitor by top is running...'

        during = int(time.clock()) - start
        if during >= g_run_time or during >= g_max_run_time:
            print 'LOOP exit, and cost %d minutes %d seconds.' %((during/60), (during%60))
            break

def run_top_cmd_main():
    f_report = MonitorUtils.g_create_and_open_report_with_append(g_report_file_path_top)

    try:
        write_single_line_report(f_report, build_report_header_for_top_cmd())
        loop_process(run_top_cmd_and_write_output, f_report)
    finally:
        write_single_line_report(f_report, build_report_trailer_for_top_cmd())
        file_close_and_flush(f_report)

def run_top_cmd_for_pkg_main():
    f_report = MonitorUtils.g_create_and_open_report_with_append(g_report_file_path_top_for_pkg)
    
    try:
        write_single_line_report(f_report, build_report_header_for_top_cmd_for_pkg())
        loop_process(run_top_cmd_for_pkg_and_write_output, f_report)
    finally:
        write_single_line_report(f_report, build_report_trailer_for_top_cmd_for_pkg())
        file_close_and_flush(f_report)

def parse_top_for_pkg_report_main():
    f_report = MonitorUtils.g_open_report_with_read(g_report_file_path_top_for_pkg)

    lines_for_total, lines_for_pkg = parse_top_for_pkg_report(read_lines_from_report(f_report))
    lines_for_total = parse_lines_for_total(lines_for_total)
    
    f_total_category = MonitorUtils.g_create_and_open_report_with_write(g_report_file_path_total_category)
    f_pkg_category = MonitorUtils.g_create_and_open_report_with_write(g_report_file_path_pkg_category)
    try:
        write_multiple_lines_report(f_total_category, lines_for_total)
        write_multiple_lines_report(f_pkg_category, lines_for_pkg)
    finally:
        file_close_and_flush(f_total_category)
        file_close_and_flush(f_pkg_category)


def cpu_monitor_top_main():
    
    init_path_vars()
    MonitorUtils.g_create_report_dir(g_report_dir_path)
  
    if g_flag_top:
        run_top_cmd_main()
    if g_flag_top_for_pkg:
        run_top_cmd_for_pkg_main()
   
    if g_flag_parse_report_for_pkg:
        parse_top_for_pkg_report_main()


if __name__ == '__main__':

    g_package_name = MonitorUtils.g_package_settings
    g_run_num = '01'
    g_run_time = 10 * MonitorUtils.g_min
    g_suffix = '%s_%s' %(MonitorUtils.g_cur_date, g_run_num)  # do not change

    g_flag_top = False
    g_flag_top_for_pkg = True
    g_flag_parse_report_for_pkg = True

    cpu_monitor_top_main()

    print 'CPU monitor by top, DONE!'
    pass
