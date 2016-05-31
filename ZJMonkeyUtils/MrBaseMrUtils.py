# -*- coding: utf-8 -*-
'''
Created on 2015-7-9

@author: zhengjin
'''

import os
import sys
import time

import MrBaseConstants
from MrBaseConstants import mr_log_dir_for_win
from MrBaseConstants import wait_time_for_device_connect
from MrBaseConstants import wait_time_for_start_activity
from MrBaseConstants import wait_time_for_ui_action

from com.android.monkeyrunner import MonkeyRunner as mr
from com.android.monkeyrunner import MonkeyDevice as md
from com.android.monkeyrunner import MonkeyImage as mi
from com.android.monkeyrunner import MonkeyView
from com.android.monkeyrunner.easy import By
from com.android.monkeyrunner.easy import EasyMonkeyDevice

from com.android.chimpchat.hierarchyviewer import HierarchyViewer
from com.android.hierarchyviewerlib.models import ViewNode

# ----------------------------------------------------
# device utils
# ----------------------------------------------------
def get_easy_device(device):
    return EasyMonkeyDevice(device)

def device_connect(device_ip):
    wait_time = wait_time_for_device_connect
    device = mr.waitForConnection(wait_time, device_ip)
    
    if not device:
        print >> sys.stderr,"fail"
        sys.exit(1)

    print 'connect to device %s' %(device_ip)
    return device

def start_activity(device, component_name):
    wait_time = wait_time_for_start_activity
    
    # component_name = 'tv.fun.master/tv.fun.master.ui.activity.MainActivity' 
    device.startActivity(component=component_name) 
    mr.sleep(wait_time)
    print 'start activity %s' %(component_name)
    
def sleep_seconds(sec):
    mr.sleep(sec)

def take_snapshot(device, num):
    suffix = 'png'
    file_path = os.path.join(mr_log_dir_for_win, ('mr_snapshot_%s_%s.%s' %(MrBaseConstants.date, num, suffix)))
    print 'snapshot save %s' %(file_path)
    
    result = device.takeSnapshot()
    result.writeToFile(file_path, suffix);

def exec_shell_command(device, cmd, timeout=3.0):
    device.shell(cmd, timeout)

# ----------------------------------------------------
# search UI controls
# ----------------------------------------------------
def get_hierarchy_viewer(device):
    return device.getHierarchyViewer()

def find_view_by_id(device, view_id):
    hierarchy_viewer = get_hierarchy_viewer(device)
    view_node = hierarchy_viewer.findViewById(view_id)
    print 'get view by id %s' %(view_id)
    
    return view_node

def get_text_by_id(device, view_id):
    hierarchy_viewer = get_hierarchy_viewer(device)
    view_node = hierarchy_viewer.findViewById(view_id)
    print 'get text view by id %s' %(view_id)

    return hierarchy_viewer.getText(view_node)

def wait_for_view_existance(device, view_id, timeout=3):
    for i in range(timeout):
        view_node = find_view_by_id(device, view_id)
        if view_node is None:
            print 'try to find object %d times, and wait 1 sec' %(i + 1)
            time.sleep(1)
        else:
            print 'True, wait for view %s existance'
            return
            
    print 'False, wait for view %s existance. Test exit'
    exit()
    
# ----------------------------------------------------
# UI actions
# ----------------------------------------------------
def press_keyboard_key(device, key, wait_time=wait_time_for_ui_action):
    device.press(key)
    sleep_seconds(wait_time)

def input_text(device, text, wait_time=wait_time_for_ui_action):
    device.type(text)
    sleep_seconds(wait_time)


if __name__ == '__main__':

    pass

