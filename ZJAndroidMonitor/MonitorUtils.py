# -*- coding: utf-8 -*-
'''
Created on 2016-6-14

@author: zhengjin

Global variables and functions for andorid monitor.
'''

import os
import time

# --------------------------------------------------------------
# Global Variables
# --------------------------------------------------------------
g_pkg_name_settings = 'tv.fun.settings'
g_pkg_name_filemanager = 'tv.fun.filemanager'
g_pkg_name_launcher = 'com.bestv.ott'

g_report_limiter = ','
g_new_line = '\n'
g_tab = '    '

g_min = 60
g_hour = 60 * g_min
g_max_run_time = 12 * g_hour

# seconds
g_short_interval = 1
g_interval = 3
g_long_interval = 5


# --------------------------------------------------------------
# Global Functions
# --------------------------------------------------------------
def g_create_report_dir(dir_path):
    print 'create report directory.'
    if os.path.exists(dir_path):
        print 'Warn, the report directory (%s) is exist!' % dir_path
    else:
        os.makedirs(dir_path)
        time.sleep(1)

def g_create_and_open_report_with_append(file_path):
    if os.path.exists(file_path):
        print 'Warn, the report file (%s) is exist, and removed!' % file_path
        os.remove(file_path)
        time.sleep(1)

    f_report = open(file_path, 'a')
    return f_report

def g_create_and_open_report_with_write(file_path):
    if os.path.exists(file_path):
        print 'Warn, the report file (%s) is exist!' % file_path

    f_report = open(file_path, 'w')  # if file not exist, create
    return f_report

def g_open_report_with_read(file_path):
    if not os.path.exists(file_path):
        print 'Error, the file (%s) is NOT exist!' % file_path
        return None
    
    f_report = open(file_path, 'r')
    return f_report

def g_get_current_datetime():
    g_datetime_format = '%y-%m-%d %H:%M:%S'
    return time.strftime(g_datetime_format)

def g_get_current_date():
    g_date_format = '%Y%m%d'
    return time.strftime(g_date_format)

def g_get_current_time():
    g_time_format = '%H:%M:%S'
    return time.strftime(g_time_format)

def g_get_report_root_path():
    return os.path.join(os.getcwd(), 'MonitorReports', g_get_current_date())


# --------------------------------------------------------------
# Main
# --------------------------------------------------------------
if __name__ == '__main__':

    print os.path.basename(__file__), 'DONE!'
