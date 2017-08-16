# -*- coding: utf-8 -*-
'''
Created on 2017-8-16

@author: zhengjin

Get FPS by shell command "service call SurfaceFlinger 1013".
Note: need root authority to run the command.
'''

import time
import re

import MonitorUtils as mutils
from ZJPyUtils import WinSysUtils as mysys

# --------------------------------------------------------------
# Variables
# --------------------------------------------------------------
DIV_FOUR_SPACES = '    '


# --------------------------------------------------------------
# Functions
# --------------------------------------------------------------
def get_current_frames():
    def _parse_hex_value(frames):
        return int(frames, 16)
    
    cmd = 'adb shell su -c service call SurfaceFlinger 1013'
    ret_content = mysys.run_sys_cmd_and_ret_content(cmd)

    ret_content = ret_content[ret_content.index('('):]
    m = re.search('[0-9|a-f]+', ret_content)
    if m is not None:
        return _parse_hex_value(m.group())
    return -1


# --------------------------------------------------------------
# Reports
# --------------------------------------------------------------
def build_report_record_line(new_data, old_data):
    cur_time = mutils.g_get_current_time()
    delta_frames = new_data - old_data
    
    # TODO: 2017/8/16
    print DIV_FOUR_SPACES.join((cur_time, str(new_data), str(delta_frames)))


# --------------------------------------------------------------
# Main process
# --------------------------------------------------------------
def monitor_process_loop(run_time, wait_time):
    def _set_start_data():
        tmp_data = get_current_frames()
        build_report_record_line(tmp_data, tmp_data)
        return tmp_data
    
    old_data = _set_start_data()
    start_time = int(time.clock())
    while 1:
        print 'FPS monitor is running ...'
        time.sleep(wait_time)
        if int(time.clock()) - start_time > run_time:
            print 'FPS monitor exit.'
            return

        new_data = get_current_frames()
        build_report_record_line(new_data, old_data)
        old_data = new_data


# --------------------------------------------------------------
# Main
# --------------------------------------------------------------
if __name__ == '__main__':
    
    run_time = 60  # seconds
    monitor_interval = 1
    
    monitor_process_loop(run_time, monitor_interval)
    
    print 'FPS monitor done!'
