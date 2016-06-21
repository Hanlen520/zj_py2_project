# -*- coding: utf-8 -*-
'''
@author: zhengjin
'''

import os
import sys
sys.path.append(os.environ['MR_PROJECT_PATH'])
import MrBaseUtils
import MrBaseMrUtils
import MrBaseConstants

easy_device = None

def testDemo02():
    
    device_ip = '172.17.5.185:5555'
#     device_series_no = '610510097998'
    activity_name = r'tv.fun.master/tv.fun.master.ui.activity.MainActivity'

    # setup
    MrBaseUtils.adb_connect_with_root(device_ip)
    device = MrBaseMrUtils.device_connect(device_ip)
    easy_device = MrBaseMrUtils.get_easy_device(device)
    MrBaseMrUtils.start_activity(device, activity_name)
    
    # test
#     actionsDemo021(BasicMrTcBase.TEST_DEVICE)
    getViewDemo022(easy_device)
#     startDiffActivity(MonkeyRunnerBase.TEST_DEVICE)
    
    # clearup
    print 'TODO'

# test the actions from device
def actionsDemo021(device):
    print 'run actionsDemo021'
    
    MrBaseMrUtils.press_keyboard_key(device, MrBaseConstants.KEY_RIGHT)
    MrBaseMrUtils.press_keyboard_key(device, MrBaseConstants.KEY_RIGHT)
    MrBaseMrUtils.press_keyboard_key(device, MrBaseConstants.KEY_UP)
    MrBaseMrUtils.press_keyboard_key(device, MrBaseConstants.KEY_DOWN)
    
    # verify
    MrBaseMrUtils.sleep_seconds(2.0)
    
# test to get the text of textview
def getViewDemo022(device):
    print 'run getViewDemo022'
    
    MrBaseMrUtils.sleep_seconds(3.0)
    view_title = MrBaseMrUtils.get_text_by_id(device, 'id/tv_master_title')
    print view_title

# test different activity
def startDiffActivity(device):
    print 'run startDiffActivity'
    
    component_Name= r'tv.fun.master/tv.fun.master.ui.activity.DeviceInfoActivity'
    MrBaseMrUtils.start_activity(device, component_Name)

    MrBaseMrUtils.press_keyboard_key(device, MrBaseConstants.KEY_DOWN)
    MrBaseMrUtils.press_keyboard_key(device, MrBaseConstants.KEY_DOWN)
    MrBaseMrUtils.press_keyboard_key(device, MrBaseConstants.KEY_DOWN)

    MrBaseMrUtils.sleep_seconds(2.0)
    MrBaseMrUtils.take_snapshot(device, r'd:\snapshoot_demo02')


if __name__ == '__main__':
    
    reload(sys)
    sys.setdefaultencoding('utf-8')

    testDemo02()
    
    pass