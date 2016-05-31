# -*- coding: utf-8 -*-
'''
@author: zhengjin
'''

import os
import sys
sys.path.append(os.environ['MR_PROJECT_PATH'])
import MrBaseConstants
import MrBaseMrUtils
import MrBaseUtils
import MrBaseTcHelper

# ----------------------------------------------------
# vars
# ----------------------------------------------------
global_easy_device = None

# ----------------------------------------------------
# test methods
# ----------------------------------------------------
# change channel from menu
def test_tvplayer_01(device):
    print '----------> start run test method test_tvplayer_01'
    exec_times = 1;
    channel_num = 16;

    component_name = 'com.mstar.tv.tvplayer.ui/.RootActivity'
    MrBaseMrUtils.start_activity(device, component_name)

    open_channel_list(device)
    for i in range(exec_times):
        print 'change channel %d times' %(i+1)
        for j in range(channel_num):
            print 'plus channel %d times' %(j+1)
            plus_channel_from_menu(device)
            do_screen_capture_at_interval(j+1)
        for k in range(channel_num):
            print 'min channel %d times' %(k+1)
            min_channel_from_menu(device)
            do_screen_capture_at_interval(k+1)

    print '----------> end run test method test_tvplayer_01'

def open_channel_list(device):
    MrBaseMrUtils.wait_for_view_existance(device, 'id/linear_layout_root', 6)
    MrBaseMrUtils.press_keyboard_key(device, MrBaseConstants.KEY_CENTER, 3)
    print 'Press enter and open channel list'

def plus_channel_from_menu(device):
    MrBaseMrUtils.press_keyboard_key(device, MrBaseConstants.KEY_DOWN)
    MrBaseMrUtils.press_keyboard_key(device, MrBaseConstants.KEY_CENTER, 3)

def min_channel_from_menu(device):
    MrBaseMrUtils.press_keyboard_key(device, MrBaseConstants.KEY_UP)
    MrBaseMrUtils.press_keyboard_key(device, MrBaseConstants.KEY_CENTER, 3)

def do_screen_capture_at_interval(interval):
    if interval % 5 == 0:
        MrBaseUtils.adb_screen_capture()


def test_tvplayer_02(device):
    print 'TODO!'

# ----------------------------------------------------
# main
# ----------------------------------------------------
def main():
    global_easy_device = MrBaseTcHelper.class_setup()
    test_tvplayer_01(global_easy_device)
    MrBaseTcHelper.class_clearup()

# ----------------------------------------------------
# MrTestBlueTooth
# ----------------------------------------------------
if __name__ == '__main__':
    
    main()
    pass
