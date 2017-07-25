# -*- coding: utf-8 -*-
'''
Created on 2017-7-25

@author: zhengjin

Generate the chart from monitor results.

'''
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MaxNLocator

import CpuMonitorTop

# --------------------------------------------------------------
# Constants
# --------------------------------------------------------------
PERF_MONITOR_CHART_TITLE = 'Performance Monitor'
X_LABEL_TIME = 'Time'


# --------------------------------------------------------------
# Functions: get source data
# --------------------------------------------------------------
def get_xy_data_from_cpu_top_log(run_num):
    results_file_path = CpuMonitorTop.get_report_file_path_top_for_pkg(run_num)
    if not os.path.exists(results_file_path):
        print 'The file (%s) does not exist!' % results_file_path
        exit(1)
    
    with open(results_file_path, 'r') as f_results_file:
        tmp_lines = f_results_file.readlines()
        # non results records start with *
        results_lines = [line for line in tmp_lines if not line.startswith('*')]
        
        x_arr = []
        y_arr = []
        for line in results_lines:
            tmp_fields = line.split()
            x_arr.append(tmp_fields[0])  # time
            cpu_usage = tmp_fields[3]
            y_arr.append(cpu_usage[:(len(cpu_usage) - 1)])

        if len(x_arr) != len(y_arr):
            print 'The numbers of elements for x_arr and y_arr do not equal!'
            exit(1)
        return x_arr, y_arr


# --------------------------------------------------------------
# Functions: generate chart
# --------------------------------------------------------------
def generate_chart_from_xy_data(x_labels, y_arr):
    tmp_figure = plt.figure()
    ax = tmp_figure.add_subplot(111)
    
    def format_fn(x_val, x_pos):
        if int(x_val) in x_arr:
            return x_labels[int(x_val)]
        else:
            return ''

    ax.xaxis.set_major_formatter(FuncFormatter(format_fn))
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    
    plt.title(PERF_MONITOR_CHART_TITLE)
    plt.xlabel(X_LABEL_TIME)
    plt.ylabel('CPU Usage%')
    
    x_arr = range(len(x_labels))
    plt.plot(x_arr, y_arr, color='red')
    plt.grid(True, color='green', linestyle='--', linewidth='1')
    plt.show()


# --------------------------------------------------------------
# Main
# --------------------------------------------------------------
def monitor_results_chart_main():
    x_arr, y_arr = get_xy_data_from_cpu_top_log(run_num)
    generate_chart_from_xy_data(x_arr, y_arr)


if __name__ == '__main__':
    
    run_num = '01'

    monitor_results_chart_main()
    
    print os.path.basename(__file__), 'DONE!'
