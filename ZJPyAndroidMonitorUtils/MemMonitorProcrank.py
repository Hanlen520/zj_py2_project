# -*- coding: utf-8 -*-
'''
Created on 2016-1-26

@author: zhengjin

Parse the memory info by using command procrank.

'''

import subprocess
import time
import MonitorUtils

# --------------------------------------------------------------
# Vars
# --------------------------------------------------------------
g_package_name = MonitorUtils.g_package_filemanager
g_key_word = 'RAM'

# TO BE SET
g_flag_build_report = True
g_flag_generate_total = True
g_flag_create_separate_report = False
g_flag_print_report = True  # if print report, not print log
g_flag_print_log = False

g_run_num = '03'
g_run_time = MonitorUtils.g_min * 10  # execution time
g_mointor_interval = 3  # seconds
g_time_out = MonitorUtils.g_min * 60  # seconds, time out is 60 mins

g_suffix = '%s_%s.txt' %(MonitorUtils.g_date, g_run_num)

g_report_dir_path = r'%s\procrank_log_%s' %(MonitorUtils.g_root_path, MonitorUtils.g_date)
g_report_file_path = '%s\procrank_log_%s' %(g_report_dir_path, g_suffix)
g_path_app = '%s\procrank_log_app_%s' %(g_report_dir_path, g_suffix)
g_path_total = '%s\procrank_log_total_%s' %(g_report_dir_path, g_suffix)
g_path_app_process = '%s\procrank_log_app_process_%s' %(g_report_dir_path, g_suffix)
g_path_app_service = '%s\procrank_log_app_service_%s' %(g_report_dir_path, g_suffix)

# --------------------------------------------------------------
# Functions: main
# --------------------------------------------------------------
def subprocess_run_cmd_procrank_with_total_v1(f_report):
    cmd = 'adb shell procrank'
    if g_flag_print_log:
        print cmd
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    p.wait()

    # write content
    limiter = ','
    content_record = ''
    content_total = ''
    flag_process_running = False

    for line in p.stdout.readlines():
        if (not flag_process_running) and (g_package_name in line):
            flag_process_running = True
            content_record = parse_record_line(line)
            continue
        if line.startswith(g_key_word):
            content_total = parse_total_line(line, limiter)
            break

    if not flag_process_running:
        content_record = 'The process (%s) is currently not running.' %(g_package_name)

    write_line_report(f_report, content_record)
    write_line_report(f_report, content_total)
    if g_flag_print_report:
        print_line_report(content_record)
        print_line_report(content_total)
    f_report.flush()

def subprocess_run_cmd_procrank_with_total_v2(f_report):
    # cannot use grep in windows command line, and use findstr instead
#     cmd = 'adb shell procrank | grep -E "filemanager|TOTAL"'
    cmd = r'adb shell procrank | findstr /r "filemanager TOTAL"'
    if g_flag_print_log:
        print cmd
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    p.wait()

    # write content
    limiter = ','
    content_record = ''
    content_service = 'null'
    content_total = ''
    
    lines = p.stdout.readlines();
    min_lines_count = 2
    if len(lines) < min_lines_count:
        content_record = 'The process (%s) is currently not running.' %(g_package_name)
        return
    
    keyword_total = 'TOTAL'
    keyword_service = 'remote'
    for line in lines:
        if (g_package_name in line) and (keyword_service not in line):
            content_record = parse_record_line(line)
        elif keyword_total in line:
            content_total = parse_total_line(line, limiter)
        else:
            content_service = parse_record_line(line)

    write_line_report(f_report, content_record)
    if content_service != 'null':
        write_line_report(f_report, content_service)
    write_line_report(f_report, content_total)
    
    if g_flag_print_report:
        print_line_report(content_record)
        if content_service != 'null':
            print_line_report(content_service)
        print_line_report(content_total)
    f_report.flush()

def subprocess_run_cmd_procrank_with_only_process(f_report):
    cmd = 'adb shell procrank | findstr %s' %(g_package_name)
    if g_flag_print_log:
        print cmd
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    p.wait()

    # write content
    flag_process_running = False
    content_record = ''
    for line in p.stdout.readlines():
        if g_package_name in line:
            flag_process_running = True
            content_record = parse_record_line(line)
            break
            
    if not flag_process_running:
        content_record = 'The process (%s) is currently not running.' %(g_package_name)
    
    write_line_report(f_report, content_record)
    if g_flag_print_report:
            print_line_report(content_record) 
    f_report.flush()

def loop_for_subprocess(fn, f_report):
    # LOOP
    start = int(time.clock())
    while True:
        time.sleep(g_mointor_interval)
        
        during = int(time.clock()) - start
        if during >= g_run_time or during >= g_time_out:
            print 'LOOP exit, and cost %d minutes %d seconds.' %((during / 60), (during % 60))
            return
        
        fn(f_report)

# --------------------------------------------------------------
# Functions: parser, format
# --------------------------------------------------------------
def parse_record_line(data):
    items = data.split()
    items_m = []
    for i in range(1, 5):
        item_k = items[i].strip()
        items_m.append(format_KtoM_for_record(item_k[0:(len(item_k) - 1)]))
        
    return '%s, %s, %s, %s, %s, %s' %(items[0], items_m[0], items_m[1], items_m[2], items_m[3], items[5])

def parse_total_line(data, limiter):
    items = data[5:].split(limiter, 6)
    items_m = []
    for item in items:
        items_m.append(format_KtoM_for_total(item.strip()))

#     return 'RAM: %s, %s, %s, %s, %s, %s' %(items_m[0], items_m[1], items_m[2], items_m[3], items_m[4], items_m[5])
    return 'RAM: %s' %(MonitorUtils.g_report_limiter.join(items_m))

def format_KtoM_for_record(item):
    mum_m = round(int(item) / 1024)
    return '%dM' %(mum_m)

def format_KtoM_for_total(item):
    index = item.find('K')
    item_m = format_KtoM_for_record(item[0:index])
    return '%s%s' %(item_m, item[(index + 1):])

# --------------------------------------------------------------
# Functions: report
# --------------------------------------------------------------

def create_report_header(f_report):
    print 'create report header.'
    
    report_title = 'Memory Monitor Report'
    content_vss = 'VSS - Virtual Set Size'
    content_rss = 'RSS - Resident Set Size'
    content_pss = 'PSS - Proportional Set Size'
    content_uss = 'USS - Unique Set Size'
    report_header = 'Time, PID, Vss, Rss, Pss, Uss, cmdline'

    f_report.write(report_title + MonitorUtils.g_new_line)
    f_report.write(content_vss + MonitorUtils.g_tab + MonitorUtils.g_tab)
    f_report.write(content_rss + MonitorUtils.g_tab + MonitorUtils.g_tab)
    f_report.write(content_pss + MonitorUtils.g_tab + MonitorUtils.g_tab)
    f_report.write(content_uss + MonitorUtils.g_new_line)
    f_report.write(report_header + MonitorUtils.g_new_line)
    f_report.flush()

def write_line_report(f_report, line):
    if g_flag_print_log:
        print 'write line to the report file.'
    f_report.write('%s%s%s%s' %(time.strftime(MonitorUtils.g_time_format), MonitorUtils.g_tab, line, MonitorUtils.g_new_line))

# print line in the console
def print_line_report(line):
    print '%s%s%s' %(time.strftime(MonitorUtils.g_time_format), MonitorUtils.g_tab, line)

def create_separate_report_for_app_and_total(f_report):
    print 'create separate report for total and APP.'
    
    lines = f_report.readlines()
    if len(lines) == 0:
        print 'The size of file is zero --> %s' %(g_report_file_path)
        exit()

    f_total = open(g_path_total, 'a')
    f_app = open(g_path_app, 'a')
    index_begin = 15
    index_end = 25
    try:
        for line in lines:
            if line.find(g_key_word,index_begin,index_end) != -1:  # find 'RAM'
                f_total.write(line)
            else:
                f_app.write(line) 
    finally:
        f_total.close()
        f_app.close()

def create_separate_report_for_process_and_service():
    print 'create separate report for app process and service.'
    
    f_app = open(g_path_app, 'r')
    try:
        lines = f_app.readlines()
    finally:
        f_app.close()

    f_len = len(lines)
    if f_len == 0:
        print 'The size of file is zero --> %s' %(g_path_app)
        exit()
    
    f_app_process = open(g_path_app_process, 'a')
    f_app_service = open(g_path_app_service, 'a')
    start_index = 3
    try:
        for i in range(start_index, f_len):
            if ((i % 2) == 0):
                f_app_service.write(lines[i])
            else:
                f_app_process.write(lines[i])
    finally:
        f_app_process.close()
        f_app_service.close()

# --------------------------------------------------------------
# Main
# --------------------------------------------------------------
def mem_monitor_procrank_main():
    
    if g_flag_build_report:
        MonitorUtils.g_create_report_dir(g_report_dir_path)
        f_report = MonitorUtils.g_create_and_open_report_with_append(g_report_file_path)

        try:
            create_report_header(f_report)
            if g_flag_generate_total:
#                 loop_for_subprocess(subprocess_run_cmd_procrank_with_total_v1, f_report)
                loop_for_subprocess(subprocess_run_cmd_procrank_with_total_v2, f_report)
            else:
                loop_for_subprocess(subprocess_run_cmd_procrank_with_only_process, f_report)
        finally:
            f_report.close()
            time.sleep(1)
    #end-if
    
    if g_flag_create_separate_report:
        f_report = MonitorUtils.g_open_report_with_read(g_report_file_path)
        try:
            create_separate_report_for_app_and_total(f_report)
        finally:
            f_report.close()
            time.sleep(1)

#         create_separate_report_for_process_and_service()
    #end-if


if __name__ == '__main__':

    # before execution, there has device connected via adb
    mem_monitor_procrank_main()
    print 'Memory monitor by procrank, DONE!'
    pass
