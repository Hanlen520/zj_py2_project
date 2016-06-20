# -*- coding: utf-8 -*-
'''
Created on 2016-1-26

@author: zhengjin

Parse and build the memory info by using procrank.

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
g_category_sevice = 'app_service'
g_category_total = 'sys_mem'

# to be set
g_flag_build_report = True
g_flag_parse_report = True

# set which to be monitor
g_flag_only_process = False
g_flag_only_total = False
g_flag_process_total = False
g_flag_all = True

g_flag_print_report = True
g_flag_print_log = False

# execution parameters set
g_run_num = '01'
g_run_time = 10 * MonitorUtils.g_min
g_time_out = 60 * MonitorUtils.g_min
g_mointor_interval = MonitorUtils.g_short_interval  # seconds

g_suffix = '%s_%s.txt' %(MonitorUtils.g_date, g_run_num)
g_report_dir_path = r'%s\procrank_mem_log_%s' %(MonitorUtils.g_root_path, MonitorUtils.g_date)
g_report_file_path = r'%s\procrank_mem_log_%s' %(g_report_dir_path, g_suffix)
g_category_report_file_path = r'%s\procrank_category_log_%s' %(g_report_dir_path, g_suffix)
g_path_total = r'%s\procrank_log_total_%s' %(g_report_dir_path, g_suffix)
g_path_app_process = r'%s\procrank_log_app_process_%s' %(g_report_dir_path, g_suffix)
g_path_app_sevice = r'%s\procrank_log_app_service_%s' %(g_report_dir_path, g_suffix)


# --------------------------------------------------------------
# Functions: run procrank command
# --------------------------------------------------------------
def run_cmd_procrank():
    cmd = 'adb shell procrank'
    if g_flag_print_log:
        print cmd
    
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    p.wait()
    lines = p.stdout.readlines()

    return lines

def run_cmd_procrank_with_findstr_keyword(find_str):
    cmd = 'adb shell procrank | findstr %s' %(find_str)
    if g_flag_print_log:
        print cmd

    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    p.wait()
    lines = p.stdout.readlines()
    
    return lines
    
def run_cmd_procrank_with_findstr_all():
    # cannot use grep in windows command line, and use findstr instead
#     cmd = 'adb shell procrank | grep -E "filemanager|TOTAL"'
    cmd_procrank = 'adb shell procrank' 
    cmd_findstr = 'findstr /r "%s %s:"' %(g_package_name, g_keyword_ram)
    cmd = '%s | %s' %(cmd_procrank, cmd_findstr)
    if g_flag_print_log:
        print cmd

    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    p.wait()
    lines = p.stdout.readlines()
    
    return lines


# --------------------------------------------------------------
# Functions: run commands and write files
# --------------------------------------------------------------
g_default_content_process = '%s null: the process (%s) is currently NOT running.' %(g_category_process, g_package_name)
g_default_content_sevice = '%s null: the sevice (%s:remote) is currently NOT running.' %(g_category_sevice, g_package_name)
g_default_content_total = '%s null: run procrank error, total line is NOT found.' %(g_category_total)

def subprocess_run_cmd_and_write_report_for_process(f_report):
    lines = run_cmd_procrank_with_findstr_keyword(g_package_name)

    content_record = g_default_content_process
    for line in lines:
        if check_is_process_line(line):
            content_record = format_prefix_with_category(g_category_process, parse_output_process_line(line))
            
    write_line_report_with_time(f_report, content_record)

def subprocess_run_cmd_and_write_report_for_total(f_report):
    lines = run_cmd_procrank_with_findstr_keyword(g_keyword_ram)

    content_record = g_default_content_total
    for line in lines:
        if check_is_total_line(line):
            content_record = format_prefix_with_category(g_category_total, parse_output_total_line(line, MonitorUtils.g_report_limiter))
            
    write_line_report_with_time(f_report, content_record)

def subprocess_run_cmd_and_write_report_for_process_and_total(f_report):
    lines = run_cmd_procrank()

    content_record = g_default_content_process
    content_total = g_default_content_total
    
    for line in lines:
        if check_is_process_line(line):
            content_record = format_prefix_with_category(g_category_process, parse_output_process_line(line))
        elif check_is_total_line(line):
            content_total = format_prefix_with_category(g_category_total, parse_output_total_line(line, MonitorUtils.g_report_limiter))

    write_line_report_with_time(f_report, content_record, content_total)

def subprocess_run_cmd_and_write_report_for_all(f_report):
    lines = run_cmd_procrank_with_findstr_all()

    content_record = g_default_content_process
    content_service = g_default_content_sevice
    content_total = g_default_content_total

    for line in lines:
        if check_is_process_line(line):
            content_record = format_prefix_with_category(g_category_process, parse_output_process_line(line))
        elif check_is_sevice_line(line):
            content_service = format_prefix_with_category(g_category_sevice, parse_output_process_line(line))
        elif check_is_total_line(line):
            content_total = format_prefix_with_category(g_category_total, parse_output_total_line(line, MonitorUtils.g_report_limiter))

    write_line_report_with_time(f_report, content_record, content_service, content_total)

def check_is_process_line(line):
    return ((g_package_name in line) and (g_keyword_sevice not in line))

def check_is_sevice_line(line):
    return ((g_package_name in line) and (g_keyword_sevice in line))

def check_is_total_line(line):
    return (line.startswith(g_keyword_ram))

def loop_for_subprocess(fn, f_report):
    # LOOP
    start = int(time.clock())

    while True:
        fn(f_report)
        time.sleep(g_mointor_interval)

        during = int(time.clock()) - start
        if during >= g_run_time or during >= g_time_out:
            print 'LOOP exit, and cost %d minutes %d seconds.' %((during/60), (during%60))
            return


# --------------------------------------------------------------
# Functions: parser and format line
# --------------------------------------------------------------
def parse_output_process_line(line):
    items = line.split()
    parse_items = []
    for i in range(1, 5):
        item = items[i].strip()
        parse_items.append(format_KtoM_for_record(item[0:(len(item) - 1)]))
    parse_items.append(items[len(items) - 1])
    
    return MonitorUtils.g_report_limiter.join(parse_items)

def parse_output_total_line(line, limiter):
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
# Functions: create report
# --------------------------------------------------------------
def create_report_header(f_report):
    if g_flag_print_log:
        print 'log: create report header.'
    
    report_title_line = '******* PROCRANK MEMORY REPORT: %s' %(g_package_name)
    report_cols_line = 'Time,Category,PID,Vss,Rss,Pss,Uss,cmdline'

    content_vss = 'VSS - Virtual Set Size'
    content_rss = 'RSS - Resident Set Size'
    content_pss = 'PSS - Proportional Set Size'
    content_uss = 'USS - Unique Set Size'
    report_exlain_line = MonitorUtils.g_tab.join((content_vss,content_rss,content_pss,content_uss))

    write_line_report(f_report,report_title_line,report_exlain_line,report_cols_line)

def create_report_trailer(f_report):
    if g_flag_print_log:
        print 'log: create report trailer.'

    trailer_line = '************** PROCRANK MEMORY REPORT END'
    write_line_report(f_report, trailer_line)

def write_line_report(f_report, *arg):
    if g_flag_print_log:
        print 'log: write line to the report file.'
    
    for line in arg:
        if g_flag_print_report:
            print line
        f_report.write('%s%s' %(line, MonitorUtils.g_new_line))

    f_report.flush()

def write_line_report_with_time(f_report, *arg):
    if g_flag_print_log:
        print 'log: write line to the report file with time.'
    
    cur_time = time.strftime(MonitorUtils.g_time_format)
    for line in arg:
        if g_flag_print_report:
            print_line_report_with_time(cur_time, line)
        f_report.write('%s,%s%s' %(cur_time, line, MonitorUtils.g_new_line))

    f_report.flush()

def print_line_report_with_time(cur_time, line):
    print '%s,%s' %(cur_time, line)


# --------------------------------------------------------------
# Functions: parse report
# --------------------------------------------------------------
def create_separated_report_for_process_service_total():
    if g_flag_print_log:
        print 'log: create separate report for APP process, service, and total.'
    
    lines = read_lines_from_file(g_report_file_path)
    if len(lines) == 0:
        print 'Error, the file size is zero --> %s' %(g_report_file_path)
        return

    f_total = MonitorUtils.g_create_and_open_report_with_write(g_path_total)
    f_process = MonitorUtils.g_create_and_open_report_with_write(g_path_app_process)
    f_sevice = MonitorUtils.g_create_and_open_report_with_write(g_path_app_sevice)
    try:
        for line in lines:
            if g_category_process in line:
                f_process.write(line)
            elif g_category_total in line:
                f_total.write(line)
            elif g_category_sevice in line:
                f_sevice.write(line)
    finally:
        files_flush_and_close(f_process,f_sevice,f_total)

def create_report_sorted_by_category():
    if g_flag_print_log:
        print 'log: create report sorted by category: APP process, service, and total.'
    
    lines = read_lines_from_file(g_report_file_path)
    if len(lines) == 0:
        print 'Error, the size of file is zero --> %s' %(g_report_file_path)
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
        elif g_category_sevice in line:
            lines_sevice.append(line)
        elif g_category_total in line:
            lines_total.append(line)
        elif keyword_end in line:
            lines_trailer.append(line)
        else:
            lines_header.append(line)

#     lines.sort(key=lambda x:x.split(',')[1])

    f_category_report = MonitorUtils.g_create_and_open_report_with_write(g_category_report_file_path)
    try:
        write_lines_into_file(f_category_report,lines_header,lines_process,lines_sevice,lines_total,lines_trailer)
    finally:
        files_flush_and_close(f_category_report)

def read_lines_from_file(g_report_file_path):
    lines = []
    f_report = MonitorUtils.g_open_report_with_read(g_report_file_path)
    try:
        lines = f_report.readlines()
    finally:
        f_report.close()
    
    return lines

def write_lines_into_file(f_report, *arg):
    for lines in arg:
        f_report.writelines(lines)

def files_flush_and_close(*arg):
    for f in arg:
        f.flush()
        f.close()


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
                loop_for_subprocess(subprocess_run_cmd_and_write_report_for_process, f_report)
            elif g_flag_only_total:
                loop_for_subprocess(subprocess_run_cmd_and_write_report_for_total, f_report)
            elif g_flag_process_total:
                loop_for_subprocess(subprocess_run_cmd_and_write_report_for_process_and_total, f_report)
            elif g_flag_all:
                loop_for_subprocess(subprocess_run_cmd_and_write_report_for_all, f_report)
            else:
                print 'Error: no monitor flag set and exit.'
                exit(1)
        finally:
            create_report_trailer(f_report)
            f_report.close()
    
    if g_flag_parse_report:
#         create_report_sorted_by_category()
        create_separated_report_for_process_service_total()


if __name__ == '__main__':

    # before execution, there has device connected via adb
    mem_monitor_procrank_main()
    print 'Memory monitor by procrank, DONE!'

    pass