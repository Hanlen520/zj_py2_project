# -*- coding: utf-8 -*-
'''
Created on 2016-6-21

@author: zhengjin

Get network up and down data flow from /proc/pid/net/dev.
'''

import os
import time

import MonitorUtils as mutils
from ZJPyUtils import WinSysUtils as mysys
from ZJPyUtils import AdbUtils as myadb

# --------------------------------------------------------------
# Variables
# --------------------------------------------------------------
INIT_NETWORK_DATA = (0, 0)

DIV_FOUR_SPACES = '    '
DIV_LINE = '*' * 30
STR_KB = ' KB'

g_data_from_beginning = INIT_NETWORK_DATA
g_data_at_end = INIT_NETWORK_DATA


# --------------------------------------------------------------
# Path Variables
# --------------------------------------------------------------
g_report_path = ''

def init_path_vars(root_path):
    global g_report_path
    g_report_path = os.path.join(root_path, 'net_data_dev_for_package.log')

def get_report_file_path_top_for_pkg(root_path):
    # invoked from external
    init_path_vars(root_path)
    return g_report_path


# --------------------------------------------------------------
# Functions
# --------------------------------------------------------------
def get_process_id_by_pkg_name(pkg_name):
    cmd = 'adb shell ps | findstr ' + pkg_name
    tmp_lines = mysys.run_sys_cmd_and_ret_lines(cmd)
    
    if len(tmp_lines) != 1:
        return '-1'
    return tmp_lines[0].split()[1]

def get_network_data_flow(pkg_name, is_wifi=False):
    ''' return (int, int) as Kb
    '''
    def _get_filter_keyword(is_wifi):
        if is_wifi:
            return 'wlan0'
        return 'eth0'

    def _parse_net_data(net_data):
        return int(net_data) / 1024

    tmp_pid = get_process_id_by_pkg_name(pkg_name)
    if tmp_pid == '-1':
        return INIT_NETWORK_DATA
    
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
            return (tmp_up_data, tmp_down_data)
    return INIT_NETWORK_DATA


# --------------------------------------------------------------
# Reports
# --------------------------------------------------------------
def build_report_header_title_line():
    return DIV_LINE + 'NETWORK DATAFLOW MONITOR REPORT: START'

def build_report_header_info_line(pkg_name, run_time):
    return '### package=%s, run_time=%s' % (pkg_name, run_time)

def build_report_cols_lines():
    return DIV_FOUR_SPACES.join(('*Time', 'TotalUp', 'DeltaUp', 'TotalDown', 'DeltaDown'))

def build_report_summary_line():
    total_up = int(g_data_at_end[0]) - int(g_data_from_beginning[0])
    total_down = int(g_data_at_end[1]) - int(g_data_from_beginning[1])
    total_data = total_up + total_down
    return '### total up data: %dkB, total down data: %dkB, total data: %dkB' % (total_up, total_down, total_data)

def build_report_trailer_line():
    return DIV_LINE + 'NETWORK DATAFLOW MONITOR REPORT: END'

def build_report_record_line(new_data, old_data):
    cur_time = mutils.g_get_current_time()
    total_up = str(new_data[0]) + STR_KB
    total_down = str(new_data[1]) + STR_KB
    delta_up = str(new_data[0] - old_data[0]) + STR_KB
    delta_down = str(new_data[1] - old_data[1]) + STR_KB
    
    return DIV_FOUR_SPACES.join((cur_time, total_up, delta_up, total_down, delta_down))

class write_utils(object):
    def __init__(self, f_report):
        self.f_report = f_report

    def write_new_lines(self, write_lines):
        if isinstance(write_lines, basestring):  # single line
            self.f_report.write(write_lines + mutils.g_new_line)
            return
    
        for line in write_lines:
            self.f_report.write(line + mutils.g_new_line)


# --------------------------------------------------------------
# Main
# --------------------------------------------------------------
def monitor_process_loop(w_instance, pkg_name, run_time, wait_time=10):
    def _set_start_data():
        tmp_data = get_network_data_flow(pkg_name)
        w_instance.write_new_lines(build_report_record_line(tmp_data, tmp_data))
        
        global g_data_from_beginning
        g_data_from_beginning = tmp_data
        
        return tmp_data
        
    def _set_end_data(old_data):
        tmp_data = get_network_data_flow(pkg_name)
        w_instance.write_new_lines(build_report_record_line(tmp_data, old_data))
        
        global g_data_at_end
        g_data_at_end = tmp_data
    
    old_data = _set_start_data()
    start_time = int(time.clock())
    while 1:
        print 'Network data monitor is running ...'
        time.sleep(wait_time)
        if int(time.clock()) - start_time > run_time:
            _set_end_data(old_data)
            print 'Network data monitor exit.'
            return

        new_data = get_network_data_flow(pkg_name)
        w_instance.write_new_lines(build_report_record_line(new_data, old_data))
        old_data = new_data

def net_monitor_setup(root_path):
    if not myadb.verify_adb_devices_connect():
        print 'Error, no adb devices connected!'
        exit(1)

    init_path_vars(root_path)
    mutils.g_create_report_dir(root_path)

def net_monitor_main(pkg_name, run_time, wait_time):
    def _write_report_header(w_instance):
        w_instance.write_new_lines(build_report_header_title_line())
        w_instance.write_new_lines(build_report_header_info_line(pkg_name, run_time))
        w_instance.write_new_lines(build_report_cols_lines())
    
    def _write_report_trailer(w_instance):
        w_instance.write_new_lines(build_report_summary_line())
        w_instance.write_new_lines(build_report_trailer_line())

    f_report = mutils.g_create_and_open_report_with_append(g_report_path)
    w_instance = write_utils(f_report)
    try:
        _write_report_header(w_instance)
        monitor_process_loop(w_instance, pkg_name, run_time, wait_time)
        _write_report_trailer(w_instance)
    finally:
        f_report.flush()
        f_report.close()


if __name__ == '__main__':
    
    run_num = '01'
    root_dir_path = r'%s\%s_%s' % (mutils.g_get_report_root_path(), mutils.g_get_current_date(), run_num)
    net_monitor_setup(root_dir_path)
    
    pkg_name = 'adbd'
    run_time = 120  # seconds
    loop_interval = 15  # default 10
    net_monitor_main(pkg_name, run_time, loop_interval)
    
    print 'Network data monitor, DONE!'
