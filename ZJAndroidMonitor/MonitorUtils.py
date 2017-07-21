# -*- coding: utf-8 -*-
'''
Created on 2016-6-14

@author: zhengjin

Global variables and functions.
'''

import os
import time

# --------------------------------------------------------------
# Global Variables
# --------------------------------------------------------------
g_pkg_name_settings = 'tv.fun.settings'
g_pkg_name_filemanager = 'tv.fun.filemanager'

g_report_limiter = ','
g_new_line = '\n'
g_tab = '    '

g_min = 60
g_date_format = '%Y%m%d'
g_time_format = '%H:%M:%S'
g_datetime_format = '%y-%m-%d %H:%M:%S'

# seconds
g_short_interval = 1
g_interval = 3
g_long_interval = 5

g_cur_date = time.strftime(g_date_format)
g_root_path = os.path.join(os.getcwd(), 'MonitorReports', g_cur_date)


# --------------------------------------------------------------
# Global Functions
# --------------------------------------------------------------
def g_create_report_dir(dir_path):
    print 'create report directory.'
    if os.path.exists(dir_path):
        print 'Warn, the report directory (%s) is exist.' % dir_path
    else:
        os.makedirs(dir_path)
        time.sleep(1)

def g_create_and_open_report_with_append(file_path):
    if os.path.exists(file_path):
        print 'Warn, the report file %s is exist.' % file_path
        os.remove(file_path)
        time.sleep(1)

    f_report = open(file_path, 'a')
    return f_report

def g_create_and_open_report_with_write(file_path):
    if os.path.exists(file_path):
        print 'Warn, the report file %s is exist.' % file_path

    f_report = open(file_path, 'w')  # if file not exist, create
    return f_report

def g_open_report_with_read(file_path):
    if not os.path.exists(file_path):
        print 'Error, the file (%s) is NOT exist.' % file_path
        exit(1)
    
    f_report = open(file_path, 'r')
    return f_report

def g_get_current_datetime():
    return time.strftime(g_datetime_format)

def g_get_current_time():
    return time.strftime(g_time_format)


# --------------------------------------------------------------
# Main
# --------------------------------------------------------------
if __name__ == '__main__':

    print os.path.basename(__file__), 'done!'
