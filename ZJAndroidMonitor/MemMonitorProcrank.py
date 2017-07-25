# -*- coding: utf-8 -*-
'''
Created on 2017-7-21

@author: zhengjin

Get the memory info by using procrank.
1) get all memory info.
2) get memory info for process.
'''

import os
import time
from ZJAndroidMonitor import MonitorUtils
from ZJPyUtils import AdbUtils

# --------------------------------------------------------------
# Variables
# --------------------------------------------------------------
RUN_TIME_OUT = 12 * MonitorUtils.g_hour

g_suffix = ''
g_report_dir_path = ''
g_report_file_for_all_path = ''
g_report_file_for_process_path = ''

def init_path_vars(run_num):
    global g_suffix
    global g_report_dir_path
    global g_report_file_for_all_path
    global g_report_file_for_process_path
    
    g_suffix = '%s_%s' % (MonitorUtils.g_cur_date, run_num)
    g_report_dir_path = r'%s\mem_procrank_log_%s' % (MonitorUtils.g_root_path, g_suffix)
    g_report_file_for_all_path = r'%s\mem_procrank_for_all_%s.txt' % (g_report_dir_path, g_suffix)
    g_report_file_for_process_path = r'%s\mem_procrank_app_process_%s.txt' % (g_report_dir_path, g_suffix)

def get_report_file_path_mem_procrank_for_process(run_num):
    init_path_vars(run_num)
    return g_report_file_for_process_path


# --------------------------------------------------------------
# Functions: run procrank command
# --------------------------------------------------------------
def run_cmd_procrank():
    cmd = 'adb shell procrank'
    return os.popen(cmd).readlines()

def run_cmd_procrank_for_pkg():
    cmd = 'adb shell procrank | findstr %s' % g_pkg_name
    tmp_lines = os.popen(cmd).readlines()
    if len(tmp_lines) != 1:
        print 'Warn, the process(%s) is not exist!' % g_pkg_name
        return None
    return tmp_lines[0]

def run_cmd_procrank_for_total_and_pkg():
    # 'adb shell procrank | grep -E "filemanager|TOTAL"'
    cmd = 'adb shell procrank | findstr /r "%s %s:"' % (g_pkg_name, 'RAM')
    return os.popen(cmd).readlines()


# --------------------------------------------------------------
# Functions: run commands and write results
# --------------------------------------------------------------
def run_cmd_and_write_report_for_process(f_report):
    tmp_line = run_cmd_procrank_for_pkg()
    if tmp_line is None:
        default_content = 'null: process (%s) NOT running.' % g_pkg_name
        write_report_line_with_time_in_file(f_report, default_content)
    write_report_line_with_time_in_file(f_report, tmp_line)

def run_cmd_and_write_report_for_all(f_report):
    f_report.writelines(build_prefix_line_for_procrank_cmd_output())
    f_report.writelines(trim_lines(run_cmd_procrank()))
    f_report.flush()

def trim_lines(input_lines):
    return [line.replace('\r\n', '\n') for line in input_lines]

def build_prefix_line_for_procrank_cmd_output():
    cur_datetime = MonitorUtils.g_get_current_datetime()
    return '%s %s\n' % (cur_datetime, '-' * 40)

def loop_for_subprocess(fn_subprocess_run_cmd, f_report):
    start = int(time.clock())
    while 1:
        fn_subprocess_run_cmd(f_report)
        time.sleep(g_monitor_interval)

        during = int(time.clock()) - start
        if during >= g_run_time or during >= RUN_TIME_OUT:
            print 'Mem monitor(procrank) exit, and cost %d minutes %d seconds.' % ((during / 60), (during % 60))
            return
        print 'Mem monitor(procrank) is running, %d minutes %d seconds.' % ((during / 60, during % 60))


# --------------------------------------------------------------
# Functions: create report and IOs
# --------------------------------------------------------------
DIV_LINE = '*' * 30

def create_and_write_report_header_for_process(f_report):
    report_title_line = DIV_LINE + ' PROCRANK MEMORY REPORT: %s' % g_pkg_name
    report_cols_line = '*Time   PID       Vss      Rss      Pss      Uss  cmdline'

    content_vss = '*VSS - Virtual Set Size,'
    content_rss = 'RSS - Resident Set Size,'
    content_pss = 'PSS - Proportional Set Size,'
    content_uss = 'USS - Unique Set Size'
    report_exlain_line = MonitorUtils.g_tab.join((content_vss, content_rss, content_pss, content_uss))

    write_report_lines_in_file(f_report, report_title_line, report_exlain_line, report_cols_line)

def create_and_write_report_header_for_all(f_report):
    report_title_line = DIV_LINE + ' PROCRANK MEMORY REPORT: START'
    write_report_lines_in_file(f_report, report_title_line)

def create_and_write_report_trailer(f_report):
    trailer_line = DIV_LINE + ' PROCRANK MEMORY REPORT: END'
    write_report_lines_in_file(f_report, trailer_line)

def write_report_lines_in_file(f_report, *arg):
    for line in arg:
        print line
        f_report.write(line + MonitorUtils.g_new_line)
    f_report.flush()

def write_report_line_with_time_in_file(f_report, write_line):
    cur_time = MonitorUtils.g_get_current_time()
    tmp_line = cur_time + '  ' + write_line.replace('\r\n', '\n')
    print tmp_line
    f_report.write(tmp_line)
    f_report.flush()

def file_flush_and_close(f_report):
    if f_report is not None:
        f_report.flush()
        f_report.close()


# --------------------------------------------------------------
# Main
# --------------------------------------------------------------
def mem_monitor_procrank_main_for_process():
    f_report = MonitorUtils.g_create_and_open_report_with_append(g_report_file_for_process_path)
    try:
        create_and_write_report_header_for_process(f_report)
        loop_for_subprocess(run_cmd_and_write_report_for_process, f_report)
        create_and_write_report_trailer(f_report)
    finally:
        file_flush_and_close(f_report)

def mem_monitor_procrank_main_for_all():
    f_report = MonitorUtils.g_create_and_open_report_with_append(g_report_file_for_all_path)
    try:
        create_and_write_report_header_for_all(f_report)
        loop_for_subprocess(run_cmd_and_write_report_for_all, f_report)
        create_and_write_report_trailer(f_report)
    finally:
        file_flush_and_close(f_report)

def mem_monitor_procrank_setup():
    if not AdbUtils.verify_adb_devices_serialno():
        print 'No adb devices connected!'
        exit(1)

    init_path_vars(g_run_num)
    MonitorUtils.g_create_report_dir(g_report_dir_path)

def mem_monitor_procrank_main():
    mem_monitor_procrank_setup()
    if g_is_process:
        mem_monitor_procrank_main_for_process()
    else:
        mem_monitor_procrank_main_for_all()


if __name__ == '__main__':

    g_pkg_name = 'tv.ismar.daisy'
    g_run_num = '01'
    g_run_time = 30 * MonitorUtils.g_min
    g_monitor_interval = MonitorUtils.g_interval

    g_is_process = True

    mem_monitor_procrank_main()

    print 'Memory monitor by procrank, DONE!'
