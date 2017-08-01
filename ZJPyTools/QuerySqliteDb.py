# -*- coding: utf-8 -*-

'''
Created on 2017-5-11

@author: zhengjin

Query data in sqlite3 DB by sql (Android).
'''

import os
import time

from ZJPyUtils import RunCmds
from ZJPyUtils import AdbUtils

# ----------------------------------------------------
# Constants
# ----------------------------------------------------
G_SQLITE_TAG = 'sqlite>'
G_FUNTV_TAG = '|fun_tv|'


# ----------------------------------------------------
# Functions
# ----------------------------------------------------
def connect_device(device_ip):
    if not AdbUtils.adb_connect_with_root(device_ip):
        raise Exception('Adb connect with root failed!')

def query_table(db_file_abs_path, sql_text):
    cmd_conn_db = 'adb shell sqlite3 ' + db_file_abs_path
    cmd_exit_db = '.quit'
    cmds = [cmd_conn_db, sql_text, cmd_exit_db]
    
    ret_content = RunCmds.run_cmds_by_communicate(cmds)
    tmp_lines = ret_content.replace('\r', '').split('\n')
    return parse_results(tmp_lines)

def parse_results(input_lines):
    ret_lst = []
    for line in input_lines:
        if line.startswith(G_SQLITE_TAG):
            tmp_val = line.split(' ')[1]
            if len(tmp_val) > 0:
                ret_lst.append(tmp_val)
        elif G_FUNTV_TAG in line:
            ret_lst.append(line)
    
    if len(ret_lst) == 0:
        raise Exception('Return value is empty.')
    return ret_lst


# ----------------------------------------------------
# Main
# ----------------------------------------------------
def get_upload_ott_statistics():
    db_file_abs_path = '/data/data/tv.fun.ottsecurity/databases/ottstatistics.db'
    
    count = query_table(db_file_abs_path, 'select count(*) from statistics;')[0]
    print 'SQL results, count:', count 
    time.sleep(1)

    if int(count) > 0:
        print 'SQL results, records:'
        ret_lines = query_table(db_file_abs_path, 'select * from statistics;')
        for line in ret_lines:
            print line


if __name__ == '__main__':
    
    is_connected_device = True
    if not is_connected_device:
        connect_device('172.17.5.79')
    
    get_upload_ott_statistics()
    
    print os.path.basename(__file__), 'DONE!'
