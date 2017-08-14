# -*- coding: utf-8 -*-
'''
Created on 2016-6-21

@author: zhengjin
'''

import time

from ZJPyUtils import WinSysUtils as mysys

# --------------------------------------------------------------
# Variables
# --------------------------------------------------------------
INIT_DATA = ('0', '0')

g_start_data = INIT_DATA
g_end_data = INIT_DATA


# --------------------------------------------------------------
# Functions
# --------------------------------------------------------------
def get_process_id_by_pkg_name(pkg_name):
    cmd = 'adb shell ps | findstr ' + pkg_name
    tmp_lines = mysys.run_sys_cmd_and_ret_lines(cmd)
    
    if len(tmp_lines) != 1:
        return '0'
    return tmp_lines[0].split()[1]

def get_network_data_flow(pkg_name, is_wifi=False):
    def _get_filter_keyword(is_wifi):
        if is_wifi:
            return 'wlan0'
        return 'eth0'

    def _parse_net_data(net_data):
        return str(int(net_data) / 1024)

    tmp_pid = get_process_id_by_pkg_name(pkg_name)
    cmd = 'adb shell cat /proc/%s/net/dev' % tmp_pid
    tmp_lines = mysys.run_sys_cmd_and_ret_lines(cmd)
    if len(tmp_lines) == 0:
        print 'Error, return empty for command => ' + cmd
        exit(1)

    filter_keyword = _get_filter_keyword(is_wifi)
    for line in tmp_lines:
        tmp_fields = line.split()
        if tmp_fields[0].strip().startswith(filter_keyword):
            tmp_up_data = _parse_net_data(tmp_fields[1])
            tmp_down_data = _parse_net_data(tmp_fields[9])
            return (tmp_up_data, tmp_down_data)  # up, down (kB)
    return INIT_DATA


# --------------------------------------------------------------
# Reports
# --------------------------------------------------------------
def print_summary_line():
    total_up = int(g_end_data[0]) - int(g_start_data[0])
    total_down = int(g_end_data[1]) - int(g_start_data[1])
    total_data = total_up + total_down
    print 'total up data: %skB, total down data: %skB, total data: %skB' % (total_up, total_down, total_data)


# --------------------------------------------------------------
# Main
# --------------------------------------------------------------
def monitor_process_loop(pkg_name, run_time, wait_time=3):
    def _set_start_data():
        global g_start_data
        g_start_data = get_network_data_flow(pkg_name)
        print g_start_data
        
    def _set_end_data():
        global g_end_data
        g_end_data = get_network_data_flow(pkg_name)
        print g_end_data
    
    _set_start_data()
    start_time = int(time.clock())
    while 1:
        print get_network_data_flow(pkg_name)
        time.sleep(wait_time)
        
        if int(time.clock()) - start_time > run_time:
            _set_end_data()
            print 'Network data monitor exit.'
            return
        print 'Network data monitor is running ...'


if __name__ == '__main__':
    
    pkg_name = 'adbd'
    run_time = 10  # seconds
    
    monitor_process_loop(pkg_name, run_time)
    print_summary_line()
    
    print 'Network data monitor, DONE!'
