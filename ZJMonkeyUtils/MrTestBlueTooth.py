# -*- coding: utf-8 -*-
'''
@author: zhengjin
'''

import os
import sys
sys.path.append(os.environ['MR_PROJECT_PATH'])
import MrBaseConstants
import MrBaseTcHelper
import MrBaseMrUtils

# ----------------------------------------------------
# vars
# ----------------------------------------------------
global_easy_device = None

# ----------------------------------------------------
# test methods
# ----------------------------------------------------
def test_bluetooth_01(device):
    print '----------> start run test method test_bluetooth_01'

    component_name = 'tv.fun.settings/.bluetooth.BluetoothSettingActivity'
    MrBaseMrUtils.start_activity(device, component_name)
    
    MrBaseMrUtils.press_keyboard_key(device, MrBaseConstants.KEY_DOWN)
    MrBaseMrUtils.press_keyboard_key(device, MrBaseConstants.KEY_CENTER)

    print '----------> end run test method test_bluetooth_01'

# ----------------------------------------------------
# monkey_test_main
# ----------------------------------------------------
def monkey_test_main():
    global_easy_device = MrBaseTcHelper.class_setup()
    test_bluetooth_01(global_easy_device)
#     BaseTcHelper.class_clearup()

# ----------------------------------------------------
# MrTestBlueTooth
# ----------------------------------------------------
if __name__ == '__main__':
    
    monkey_test_main()
    pass
