# -*- coding: utf-8 -*-
'''
@author: zhengjin
'''

import MrBaseUtils
import MrBaseMrUtils
import MrBaseConstants

global_device = None
global_easy_device = None

# ----------------------------------------------------
# Setup
# ----------------------------------------------------
def class_setup():
    MrBaseUtils.adb_connect_with_root(MrBaseConstants.device_ip)
    global_device = MrBaseMrUtils.device_connect(MrBaseConstants.device_no)
    global_easy_device = MrBaseMrUtils.get_easy_device(global_device)
    
    if global_easy_device == None:
        print 'Error when get the mr device object!'
        exit()
    else:
        prepare_env()
        return global_easy_device

def prepare_env():
    # for shell
    MrBaseUtils.remove_dir_for_shell(MrBaseConstants.mr_log_dir_for_shell)
    MrBaseUtils.mkdir_for_shell(MrBaseConstants.captures_dir_for_shell)

    # for win
    MrBaseUtils.create_log_dir_for_win(MrBaseConstants.mr_log_dir_for_win)

# ----------------------------------------------------
# Clear up
# ----------------------------------------------------
def class_clearup():
    MrBaseUtils.adb_pull_logs_from_shell()
    MrBaseUtils.adb_disconnect_device()


if __name__ == '__main__':
    
    pass