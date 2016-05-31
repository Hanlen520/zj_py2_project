# -*- coding: utf-8 -*-

'''
@author: zhengjin
'''

import time
import os

# ----------------------------------------------------
# vars to be update
# ----------------------------------------------------
device_ip = '172.16.89.91'
device_port = '5555'
device_no = '%s:%s' %(device_ip, device_port)

date = time.strftime("%Y%m%d")
num = '01'

wait_time_for_device_connect = 3.0  # secs
wait_time_for_start_activity = 3.0  # secs
wait_time_for_ui_action = 1.0  # secs

# set log level for logcat, default is I
log_level = 'I'

mr_log_dir_for_win = r'D:\files_logs\mr_logs_%s_%s' %(date, num)
mr_log_file_for_win = os.path.join(mr_log_dir_for_win, ('mr_log_%s_%s.log' %(date, num)))

mr_log_dir_for_shell = '/sdcard/testlogs/mr_logs'
mr_logcat_file_for_shell = '%s/mr_logcat_%s_%s.log' %(mr_log_dir_for_shell, date, num)

# screen captures path
captures_dir_for_win = r'%s\captures' %(mr_log_dir_for_win)
captures_dir_for_shell = '%s/captures' %(mr_log_dir_for_shell)
capture_for_shell = '%s/capture_%s' %(captures_dir_for_shell, date)

# ----------------------------------------------------
# keycodes
# ----------------------------------------------------
KEY_ENTER = 'KEYCODE_ENTER'
KEY_HOME = 'KEYCODE_HOME'
KEY_BACK = 'KEYCODE_BACK'
KEY_UP = 'KEYCODE_DPAD_UP'
KEY_DOWN = 'KEYCODE_DPAD_DOWN'
KEY_LEFT = 'KEYCODE_DPAD_LEFT'
KEY_RIGHT = 'KEYCODE_DPAD_RIGHT'
KEY_CENTER = 'KEYCODE_DPAD_CENTER'
KEY_CHANNEL_PLUS = 'KEYCODE_CHANNEL_UP'  # 166
KEY_CHANNEL_MIN = 'KEYCODE_CHANNEL_DOWN'  # 167
KEY_TV = 'unknown'

