# -*- coding: utf-8 -*-
'''
Created on 2017-7-25

@author: zhengjin

Generate the chart from monitor results.

'''
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MaxNLocator

import MonitorUtils, CpuMonitorTop, MemMonitorProcrank, MemMonitorDumpsys

# --------------------------------------------------------------
# Constants
# --------------------------------------------------------------
PERF_MONITOR_CHART_TITLE = 'Performance Monitor'
X_LABEL_TIME = 'Execution Time'
ERROR_MSG_ARR_LENGTH_NOT_EQUAL = 'Error, the numbers of elements for x_arr and y_arr do not equal!'

PKG_NAME = 'null'
MONITOR_INTERVAL = 'null'


# --------------------------------------------------------------
# Functions: get source data
# --------------------------------------------------------------
def get_xy_data_from_cpu_top_log(run_num, root_path):
    results_file_path = CpuMonitorTop.get_report_file_path_top_for_pkg(run_num, root_path)
    results_lines = get_results_lines_from_src_file(results_file_path)
    
    x_arr = []
    y_arr = []
    for line in results_lines:
        tmp_fields = line.split()
        x_arr.append(tmp_fields[0])  # time
        cpu_usage = tmp_fields[3]
        y_arr.append(cpu_usage[:(len(cpu_usage) - 1)])

    if len(x_arr) != len(y_arr):
        print ERROR_MSG_ARR_LENGTH_NOT_EQUAL
        exit(1)
    return x_arr, y_arr

def get_xy_data_from_mem_procrank_log(run_num, root_path):
    results_file_path = MemMonitorProcrank.get_report_file_path_mem_procrank_for_process(run_num, root_path)
    results_lines = get_results_lines_from_src_file(results_file_path)
    
    x_arr = []
    y_arr = []
    for line in results_lines:
        tmp_fields = line.split()
        x_arr.append(tmp_fields[0])
        mem_uss = tmp_fields[5]
        y_arr.append(format_mem_value(mem_uss))

    if len(x_arr) != len(y_arr):
        print ERROR_MSG_ARR_LENGTH_NOT_EQUAL
        exit(1)
    return x_arr, y_arr

def get_xy_data_from_mem_dumpsys_log(run_num, root_path):
    results_file_path = MemMonitorDumpsys.get_report_file_path_mem_dumpsys(run_num, root_path)
    results_lines = get_results_lines_from_src_file(results_file_path)
    
    x_arr = []
    y_arr = []
    for line in results_lines:
        tmp_fields = line.split(',')
        x_arr.append(tmp_fields[0])
        mem_pss = tmp_fields[1]
        y_arr.append(format_mem_value(mem_pss))

    if len(x_arr) != len(y_arr):
        print ERROR_MSG_ARR_LENGTH_NOT_EQUAL
        exit(1)
    return x_arr, y_arr

def format_mem_value(mem_val):
    tmp_val = mem_val[:(len(mem_val) - 1)]  # delete K
    return round(float(tmp_val) / 1024, 2)

def get_results_lines_from_src_file(src_file_path):
    if not os.path.exists(src_file_path):
        print 'Error, the file (%s) does not exist!' % src_file_path
        exit(1)
    
    with open(src_file_path, 'r') as f_results_file:
        tmp_lines = f_results_file.readlines()
        parse_info_line_and_set_global_vars(tmp_lines)  # get package name and interval
        
        results_lines = [line for line in tmp_lines if verify_record_line(line)]
        if len(results_lines) == 0:
            print 'Error, the file (%s) is empty!' % src_file_path
            exit(1)
        return results_lines

def verify_record_line(line):
    if not line.startswith('*') and not line.startswith('###'):
        return True
    return False

def parse_info_line_and_set_global_vars(input_lines):
    global PKG_NAME
    global MONITOR_INTERVAL
    
    for line in input_lines:
        if line.startswith('###'):
            kvs = line.split()
            PKG_NAME = kvs[1].split('=')[1]
            MONITOR_INTERVAL = kvs[2].split('=')[1]
            return


# --------------------------------------------------------------
# Functions: generate chart
# --------------------------------------------------------------
def generate_chart_from_xy_data(x_labels, y_arr, y_label_text):
    tmp_figure = plt.figure()
    ax = tmp_figure.add_subplot(111)
    
    def format_fn(x_val, x_pos):
        if int(x_val) in x_arr:
            return x_labels[int(x_val)]
        else:
            return ''

    ax.xaxis.set_major_formatter(FuncFormatter(format_fn))
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    
    plt.title('%s (%s)' % (PERF_MONITOR_CHART_TITLE, PKG_NAME))
    plt.xlabel('%s (per %s seconds)' % (X_LABEL_TIME, MONITOR_INTERVAL))
    plt.ylabel(y_label_text)
    
    x_arr = range(len(x_labels))
    plt.plot(x_arr, y_arr, color='red')
    plt.grid(True, color='green', linestyle='--', linewidth='1')
    plt.show()


# --------------------------------------------------------------
# Main
# --------------------------------------------------------------
def create_monitor_results_chart_for_cpu_top_main():
    x_arr, y_arr = get_xy_data_from_cpu_top_log(run_num, get_report_root_dir_path())
    y_label_text = 'CPU Usage%'
    generate_chart_from_xy_data(x_arr, y_arr, y_label_text)

def create_monitor_results_chart_for_mem_procrank_main():
    x_arr, y_arr = get_xy_data_from_mem_procrank_log(run_num, get_report_root_dir_path())
    y_label_text = 'Memory Usage - USS (MB)'
    generate_chart_from_xy_data(x_arr, y_arr, y_label_text)

def create_monitor_results_chart_for_mem_dumpsys_main():
    x_arr, y_arr = get_xy_data_from_mem_dumpsys_log(run_num, get_report_root_dir_path())
    y_label_text = 'Memory Usage - PSS (MB)'
    generate_chart_from_xy_data(x_arr, y_arr, y_label_text)

def get_report_root_dir_path():
    try:
        global report_root_path
        return report_root_path
    except Exception:
        return MonitorUtils.g_get_report_root_path()

def monitor_results_chart_main():
    if is_create_monitor_chart_for_cpu_top:
        create_monitor_results_chart_for_cpu_top_main()
    elif is_create_monitor_chart_for_mem_procrank:
        create_monitor_results_chart_for_mem_procrank_main()
    elif is_create_monitor_chart_for_mem_dumpsys:
        create_monitor_results_chart_for_mem_dumpsys_main()


if __name__ == '__main__':
    
    run_num = '01'
#     report_root_path = r'E:\Eclipse_Workspace\ZJPyProject\ZJMonkeyTest\MonkeyReprots\20170726\20170726_01\profile_logs'

    is_create_monitor_chart_for_cpu_top = True
    is_create_monitor_chart_for_mem_procrank = True
    is_create_monitor_chart_for_mem_dumpsys = False

    monitor_results_chart_main()

    print os.path.basename(__file__), 'DONE!'
