# -*- coding: utf-8 -*-
'''
Created on 2016-1-26

@author: zhengjin

Parse the memory info by using command procrank.

'''

import subprocess
import time

from ZJPyAndroidMonitorUtils import MonitorUtils

# --------------------------------------------------------------
# Vars
# --------------------------------------------------------------
g_package_name = MonitorUtils.g_package_filemanager   # to be set
g_keyword_ram = 'RAM'
g_keyword_sevice = 'remote'

g_category_process = 'app_process'
g_category_service = 'app_service'
g_category_total = 'sys_mem'

# to be set
g_flag_build_report = True
g_flag_create_separate_report = False
g_flag_only_process = True
g_flag_print_report = True  # if print report, not print log
g_flag_print_log = False

g_run_num = '01'  # to be set
g_run_time = 2 * MonitorUtils.g_min  # to be set 
g_time_out = 60 * MonitorUtils.g_min
g_mointor_interval = 5  # seconds

g_suffix = '%s_%s.txt' %(MonitorUtils.g_date, g_run_num)
g_report_dir_path = r'%s\procrank_log_%s' %(MonitorUtils.g_root_path, MonitorUtils.g_date)
g_report_file_path = '%s\procrank_log_%s' %(g_report_dir_path, g_suffix)
g_category_report_file_path = '%s\procrank_category_log_%s' %(g_report_dir_path, g_suffix)
g_path_total = '%s\procrank_log_total_%s' %(g_report_dir_path, g_suffix)
g_path_app_process = '%s\procrank_log_app_process_%s' %(g_report_dir_path, g_suffix)
g_path_app_sevice = '%s\procrank_log_app_service_%s' %(g_report_dir_path, g_suffix)


# --------------------------------------------------------------
# Functions: main logic
# --------------------------------------------------------------
def subprocess_run_cmd_procrank_with_total_v1(f_report):
    cmd = 'adb shell procrank'
    if g_flag_print_log:
        print cmd
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    p.wait()

    # write content
    limiter = ','
    content_record = 'null'
    content_total = ''

    for line in p.stdout.readlines():
        if (g_package_name in line) and (g_keyword_sevice not in line):
            content_record = format_prefix_with_category(g_category_process, parse_record_line(line))
        elif line.startswith(g_keyword_ram):
            content_total = format_prefix_with_category(g_category_total, parse_total_line(line, limiter))
            break

    if content_record == 'null':
        content_record = 'The process (%s) is currently not running.' %(g_package_name)

    write_line_report(f_report, content_record)
    write_line_report(f_report, content_total)
    f_report.flush()

def subprocess_run_cmd_procrank_with_total_v2(f_report):
    # cannot use grep in windows command line, and use findstr instead
#     cmd = 'adb shell procrank | grep -E "filemanager|TOTAL"'
    cmd = 'adb shell procrank | findstr /r "%s %s:"' %(g_package_name, g_keyword_ram)
    if g_flag_print_log:
        print cmd
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    p.wait()

    # write content
    limiter = ','
    content_record = ''
    content_service = 'null'
    content_total = ''
    
    lines = p.stdout.readlines()
    min_lines_count = 2
    if len(lines) < min_lines_count:
        content_record = 'The process (%s) is currently not running.' %(g_package_name)
        return
    
    for line in lines:
        if (g_package_name in line) and (g_keyword_sevice not in line):
            content_record = format_prefix_with_category(g_category_process, parse_record_line(line))
        elif g_keyword_ram in line:
            content_total = format_prefix_with_category(g_category_total, parse_total_line(line, limiter))
        else:
            content_service = format_prefix_with_category(g_category_service, parse_record_line(line))

    write_line_report(f_report, content_record)
    if content_service != 'null':
        write_line_report(f_report, content_service)
    write_line_report(f_report, content_total)
    f_report.flush()

def subprocess_run_cmd_procrank_with_only_process(f_report):
    cmd = 'adb shell procrank | findstr %s' %(g_package_name)
    if g_flag_print_log:
        print cmd
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    p.wait()

    # write content
    content_record = 'null'
    for line in p.stdout.readlines():
        if (g_package_name in line) and (g_keyword_sevice not in line):
            content_record = format_prefix_with_category(g_category_process, parse_record_line(line))
            break
            
    if content_record == 'null':
        content_record = 'The process (%s) is currently not running.' %(g_package_name)
    
    write_line_report(f_report, content_record)
    f_report.flush()

def loop_for_subprocess(fn, f_report):
    # LOOP
    start = int(time.clock())
    while True:
        fn(f_report)
        time.sleep(g_mointor_interval)

        during = int(time.clock()) - start
        if during >= g_run_time or during >= g_time_out:
            print 'LOOP exit, and cost %d minutes %d seconds.' %((during / 60), (during % 60))
            return

# --------------------------------------------------------------
# Functions: parser and format
# --------------------------------------------------------------
def parse_record_line(line):
    items = line.split()
    parse_items = []
    for i in range(1, 5):
        item = items[i].strip()
        parse_items.append(format_KtoM_for_record(item[0:(len(item) - 1)]))
    parse_items.append(items[len(items) - 1])
    
    return MonitorUtils.g_report_limiter.join(parse_items)

def parse_total_line(line, limiter):
    items = line[5:].split(limiter, 6)
    parse_items = []
    for item in items:
        parse_items.append(format_KtoM_for_total(item.strip()))

    return MonitorUtils.g_report_limiter.join(parse_items)

def format_KtoM_for_record(item):
    mum_m = round(int(item) / 1024)
    return '%dM' %(mum_m)

def format_KtoM_for_total(item):
    index = item.find('K')
    item_m = format_KtoM_for_record(item[0:index])
    return '%s%s' %(item_m, item[(index + 1):])

def format_prefix_with_category(category, line):
    return '%s,%s' %(category, line)


# --------------------------------------------------------------
# Functions: IO
# --------------------------------------------------------------
def create_report_header(f_report):
    if g_flag_print_log:
        print 'log: create report header.'
    
    report_title = '******* PROCRANK MEMORY REPORT: %s' %(g_package_name)
    content_vss = 'VSS - Virtual Set Size'
    content_rss = 'RSS - Resident Set Size'
    content_pss = 'PSS - Proportional Set Size'
    content_uss = 'USS - Unique Set Size'
    report_header = 'Time,Category,PID,Vss,Rss,Pss,Uss,cmdline'

    f_report.write(report_title + MonitorUtils.g_new_line)
    f_report.write(content_vss + MonitorUtils.g_tab + MonitorUtils.g_tab)
    f_report.write(content_rss + MonitorUtils.g_tab + MonitorUtils.g_tab)
    f_report.write(content_pss + MonitorUtils.g_tab + MonitorUtils.g_tab)
    f_report.write(content_uss + MonitorUtils.g_new_line)
    f_report.write(report_header + MonitorUtils.g_new_line)
    f_report.flush()

def create_report_trailer(f_report):
    if g_flag_print_log:
        print 'log: create report trailer.'

    trailer_line = '************** PROCRANK MEMORY REPORT END'
    f_report.write(trailer_line)
    f_report.flush()

def write_line_report(f_report, line):
    if g_flag_print_log:
        print 'write line to the report file.'
    
    cur_time = time.strftime(MonitorUtils.g_time_format)
    if g_flag_print_report:
        print_line_report(cur_time, line)
    
    f_report.write('%s,%s%s' %(cur_time, line, MonitorUtils.g_new_line))

# print line in the console
def print_line_report(cur_time, line):
    print '%s,%s' %(cur_time, line)

def create_separated_report_for_process_service_total(flag_sevice=False):
    if g_flag_print_log:
        print 'log: create separate report for APP process, service, and total.'
    
    lines = []
    f_report = MonitorUtils.g_open_report_with_read(g_report_file_path)
    try:
        lines = f_report.readlines()
    finally:
        f_report.close()
    
    if len(lines) == 0:
        print 'The size of file is zero --> %s' %(g_report_file_path)
        return

    f_total = MonitorUtils.g_create_and_open_report_with_write(g_path_total)
    f_process = MonitorUtils.g_create_and_open_report_with_write(g_path_app_process)
    f_sevice = None
    if flag_sevice:
        f_sevice = MonitorUtils.g_create_and_open_report_with_write(g_path_app_sevice)

    try:
        for line in lines:
            if g_category_process in line:
                f_process.write(line)
            elif g_category_total in line:
                f_total.write(line)
            elif g_category_service in line:
                f_sevice.write(line)
    finally:
        f_process.flush()
        f_process.close()
        f_total.flush()
        f_total.close()
        if f_sevice is not None:
            f_sevice.flush()
            f_sevice.close()

def create_report_sorted_by_category():
    if g_flag_print_log:
        print 'log: create report sorted by category: APP process, service, and total.'
    
    lines = []
    f_report = MonitorUtils.g_open_report_with_read(g_report_file_path)
    try:
        lines = f_report.readlines()
    finally:
        f_report.close()
    
    if len(lines) == 0:
        print 'The size of file is zero --> %s' %(g_report_file_path)
        return

    lines_process = []
    lines_sevice = []
    lines_total = []
    lines_header = []
    lines_trailer = []
    keyword_end = 'END'
    for line in lines:
        if g_category_process in line:
            lines_process.append(line)
        elif g_category_service in line:
            lines_sevice.append(line)
        elif g_category_total in line:
            lines_total.append(line)
        elif keyword_end in line:
            lines_trailer.append(line)
        else:
            lines_header.append(line)

#     lines.sort(key=lambda x:x.split(',')[1])

    f_category_report = open(g_category_report_file_path, 'w')
    try:
        f_category_report.writelines(lines_header)
        f_category_report.writelines(lines_process)
        f_category_report.writelines(lines_sevice)
        f_category_report.writelines(lines_total)
        f_category_report.writelines(lines_trailer)
    finally:
        f_category_report.flush()
        f_category_report.close()


# --------------------------------------------------------------
# Main
# --------------------------------------------------------------
def mem_monitor_procrank_main():
    
    if g_flag_build_report:
        MonitorUtils.g_create_report_dir(g_report_dir_path)
        f_report = MonitorUtils.g_create_and_open_report_with_append(g_report_file_path)

        try:
            create_report_header(f_report)
            if g_flag_only_process:
                loop_for_subprocess(subprocess_run_cmd_procrank_with_only_process, f_report)
            else:
#                 loop_for_subprocess(subprocess_run_cmd_procrank_with_total_v1, f_report)
                loop_for_subprocess(subprocess_run_cmd_procrank_with_total_v2, f_report)
        finally:
            create_report_trailer(f_report)
            f_report.close()
    
    if g_flag_create_separate_report:
#         create_report_sorted_by_category()
        flag_sevice = True
        create_separated_report_for_process_service_total(flag_sevice)


if __name__ == '__main__':

    # before execution, there has device connected via adb
    mem_monitor_procrank_main()
    print 'Memory monitor by procrank, DONE!'

    pass