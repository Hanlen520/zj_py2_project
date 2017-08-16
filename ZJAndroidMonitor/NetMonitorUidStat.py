# -*- coding: utf-8 -*-
'''
Created on 2017-8-16

@author: zhengjin

Get network receive and send tcp data flow from /proc/uid_stat/<UID>/
'''

import time

import MonitorUtils as mutils
from ZJPyUtils import WinSysUtils as mysys

# --------------------------------------------------------------
# Variables
# --------------------------------------------------------------
STR_KB = ' KB'
DIV_FOUR_SPACES = '    '


# --------------------------------------------------------------
# Functions
# --------------------------------------------------------------
def get_uid_by_package_name(pkg_name):
    cmd = 'adb shell su -c cat /data/system/packages.list | findstr ' + pkg_name
    ret_lines = mysys.run_sys_cmd_and_ret_lines(cmd)
    
    if len(ret_lines) != 1:
        print 'Error, return empty from packages.list for package:', pkg_name
        exit(1)

    return ret_lines[0].split()[1]

def get_net_receive_data_by_uid(uid):
    cmd = 'adb shell cat /proc/uid_stat/%s/tcp_rcv' % uid
    ret_content = mysys.run_sys_cmd_and_ret_content(cmd)
    return ret_content.strip()

def get_net_send_data_by_uid(uid):
    cmd = 'adb shell cat /proc/uid_stat/%s/tcp_snd' % uid
    ret_content = mysys.run_sys_cmd_and_ret_content(cmd)
    return ret_content.strip()

def get_net_receive_send_data_by_uid(uid):
    ''' return: (int receive, int send), KB
    '''
    def _parse_data(net_data):
        return int(net_data) / 1024
    
    data_receive = get_net_receive_data_by_uid(uid)
    data_send = get_net_send_data_by_uid(uid)
    return (_parse_data(data_receive), _parse_data(data_send))


# --------------------------------------------------------------
# Reports
# --------------------------------------------------------------
def build_report_record_line(new_data, old_data):
    cur_time = mutils.g_get_current_time()
    total_receive = str(new_data[0]) + STR_KB
    total_send = str(new_data[1]) + STR_KB
    delta_receive = str(new_data[0] - old_data[0]) + STR_KB
    delta_send = str(new_data[1] - old_data[1]) + STR_KB

    # TODO: 2017/8/16
    print DIV_FOUR_SPACES.join((cur_time, total_receive, delta_receive, total_send, delta_send))


# --------------------------------------------------------------
# Main process
# --------------------------------------------------------------
def monitor_process_loop(pkg_name, run_time, wait_time):
    def _set_start_data(uid):
        tmp_data = get_net_receive_send_data_by_uid(uid)
        build_report_record_line(tmp_data, tmp_data)
        return tmp_data
    
    uid = get_uid_by_package_name(pkg_name)
    
    old_data = _set_start_data(uid)
    start_time = int(time.clock())
    while 1:
        print 'Network data monitor is running ...'
        time.sleep(wait_time)
        if int(time.clock()) - start_time > run_time:
            print 'Network data monitor exit.'
            return

        new_data = get_net_receive_send_data_by_uid(uid)
        build_report_record_line(new_data, old_data)
        old_data = new_data

def net_monitor_uid_stat_main():
    pass


# --------------------------------------------------------------
# Main
# --------------------------------------------------------------
if __name__ == '__main__':

    pkg_name = "com.infocus.nova.launcher"
    run_time = 60  # seconds
    wait_time = 10
    
    monitor_process_loop(pkg_name, run_time, wait_time)
    
    print 'Network data monitor, DONE!'
