'''
Created on 2016-6-14

@author: zhengjin
'''

import time
import os

# --------------------------------------------------------------
# Global Vars
# --------------------------------------------------------------

g_package_settings = 'tv.fun.settings'
g_package_filemanager = 'tv.fun.filemanager'

g_min = 60
g_report_limiter = ', '
g_new_line = '\n'
g_tab = '\t'

g_time_format = '%y-%m-%d,%H:%M:%S'
g_date = time.strftime('%Y%m%d')

g_root_path = r'd:\files_logs\profile_memory'

# --------------------------------------------------------------
# Global Functions
# --------------------------------------------------------------
def g_create_report_dir(dir_path):
    print 'create report directory.'
    if os.path.exists(dir_path):
        print 'The directory (%s) is exist.' %(dir_path)
    else:
        os.mkdir(dir_path)
        time.sleep(1)

def g_create_and_open_report_with_append(file_path):
    if os.path.exists(file_path):
        print 'The report file %s is exist.' %(file_path)
        suffix = 'backup'
        os.rename(file_path, ("%s_%s" %(file_path, suffix)))
        time.sleep(1)

    f_report = open(file_path, 'a')
    return f_report

def g_open_report_with_read(file_path):
    if not os.path.exists(file_path):
        print 'The file is not exist --> %s' %(file_path)
        exit()
    
    f_report = open(file_path, 'r')
    return f_report


if __name__ == '__main__':

    pass