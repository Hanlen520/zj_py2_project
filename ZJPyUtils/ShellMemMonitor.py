# -*- coding: utf-8 -*-
'''
Created on 2016-1-26

@author: zhengjin

Parse the memory info by using command procrank.

'''

import os
import subprocess
import time

# --------------------------------------------------------------
# Vars
# --------------------------------------------------------------
g_package_settings = 'tv.fun.settings'
g_package_filemanager = 'tv.fun.filemanager'

g_package_name = g_package_filemanager
g_key_word = 'RAM'

g_report_limiter = ', '
g_new_line = '\n'
g_tab = '\t'
g_time_format = '%y-%m-%d,%H:%M:%S'

# TO BE SET
g_flag_build_report = True
g_flag_generate_total = True
g_flag_create_separate_report = False
g_flag_print_report = True  # if print report, not print log
g_flag_print_log = False

g_min = 60
g_time_out = g_min * 60  # seconds, time out is 60 mins
g_run_time = g_min * 20  # execution time
g_mointor_interval = 3  # seconds

g_run_num = '02'
g_date = time.strftime('%Y%m%d')
g_suffix = '%s_%s.txt' %(g_date, g_run_num)

g_log_path = r'd:\files_logs\profile_memory\procrank_log_%s_%s' %(g_date, g_run_num)
g_report_path = '%s\procrank_log_%s' %(g_log_path, g_suffix)
g_path_app = '%s\procrank_log_app_%s' %(g_log_path, g_suffix)
g_path_total = '%s\procrank_log_total_%s' %(g_log_path, g_suffix)
g_path_app_process = '%s\procrank_log_app_process_%s' %(g_log_path, g_suffix)
g_path_app_service = '%s\procrank_log_app_service_%s' %(g_log_path, g_suffix)

# --------------------------------------------------------------
# Functions: main
# --------------------------------------------------------------
def subprocess_run_cmd_procrank_with_total(f_report):
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
    return 'RAM: %s' %(g_report_limiter.join(items_m))

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
def create_report_dir():
    print 'create report directory.'
    if os.path.exists(g_log_path):
        print 'The directory (%s) is exist.' %(g_log_path)
        exit()
        
    os.mkdir(g_log_path)
    time.sleep(1)

def open_report_with_append():
    if os.path.exists(g_report_path):
        os.remove(g_report_path)
        time.sleep(1)

    f_report = open(g_report_path, 'a')
    return f_report

def open_report_with_read():
    if not os.path.exists(g_report_path):
        print 'The file is not exist --> %s' %(g_report_path)
        exit()
    
    f_report = open(g_report_path, 'r')
    return f_report

def create_report_header(f_report):
    print 'create report header.'
    
    report_title = 'Memory Monitor Report'
    content_vss = 'VSS - Virtual Set Size'
    content_rss = 'RSS - Resident Set Size'
    content_pss = 'PSS - Proportional Set Size'
    content_uss = 'USS - Unique Set Size'
    report_header = 'Time, PID, Vss, Rss, Pss, Uss, cmdline'

    f_report.write(report_title + g_new_line)
    f_report.write(content_vss + g_tab + g_tab)
    f_report.write(content_rss + g_tab + g_tab)
    f_report.write(content_pss + g_tab + g_tab)
    f_report.write(content_uss + g_new_line)
    f_report.write(report_header + g_new_line)
    f_report.flush()

def write_line_report(f_report, line):
    if g_flag_print_log:
        print 'write line to the report file.'
    f_report.write('%s%s%s%s' %(time.strftime(g_time_format), g_tab, line, g_new_line))

# print line in the console
def print_line_report(line):
    print '%s%s%s' %(time.strftime(g_time_format), g_tab, line)

def create_separate_report_for_app_and_total(f_report):
    print 'create separate report for total and APP.'
    
    lines = f_report.readlines()
    if len(lines) == 0:
        print 'The size of file is zero --> %s' %(g_report_path)
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
def test_main():
    
    if g_flag_build_report:
        create_report_dir()
        f_report = open_report_with_append()

        try:
            create_report_header(f_report)
            if g_flag_generate_total:
                loop_for_subprocess(subprocess_run_cmd_procrank_with_total, f_report)
            else:
                loop_for_subprocess(subprocess_run_cmd_procrank_with_only_process, f_report)
        finally:
            f_report.close()
            time.sleep(1)
    #end-if
    
    if g_flag_create_separate_report:
        f_report = open_report_with_read()
        try:
            create_separate_report_for_app_and_total(f_report)
        finally:
            f_report.close()
            time.sleep(1)

#         create_separate_report_for_process_and_service()
    #end-if

    print 'Memory monitor DONE!'


if __name__ == '__main__':

    # before execution, there has device adb connected
    test_main()
    pass