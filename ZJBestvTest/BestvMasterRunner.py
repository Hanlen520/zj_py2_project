# -*- coding: utf-8 -*-
'''
Created on 2015.2.27

@author: zhengjin
'''

import os
import subprocess
import time
import datetime
# import shutil

def CreateTestResultsDir(base_path):
    res_path = base_path + os.path.sep + GetDateTime() + os.path.sep
    if (not os.path.exists(res_path)):
            os.mkdir(res_path)

    return res_path

def GetDateTime():
    now = datetime.datetime.now()
    year = now.year
    
    month = '00'
    if (now.month < 10):
        month = '0' + str(now.month)
    else:
        month = str(now.month)
    
    day = '00'
    if (now.day < 10):
        day = '0' + str(now.day)
    else:
        day = str(now.day)
    
    return '%s%s%s' %(year, month, day)

def RunTestSuite(ts_name):
    cmd = "adb shell am instrument -w " + ts_name
    p = subprocess.Popen(cmd, shell=False)
    print("Test suite -> " + ts_name + " is running...")
    p.wait()
    time.sleep(2)

def PullDataFromSDCard(shell_path, win_local_path):
    cmd = 'adb pull ' + shell_path + ' ' + win_local_path
    p = subprocess.Popen(cmd, shell=False)
    print('pull data from sdcard...')
    p.wait()
    time.sleep(2)

def RunMain():
    shell_robo_path = r'/sdcard/robotium'
    shell_robo_shotcut_path = r'/sdcard/Robotium-Screenshots'
    win_base_path = r'D:\Robotium_Test_Results'
    
    win_local_path = CreateTestResultsDir(win_base_path)
    try:
        RunTestSuite('tv.fun.master.test/tv.fun.master.testrunner.TestFunMasterRunner')
    finally:
        PullDataFromSDCard(shell_robo_path, win_local_path)
        PullDataFromSDCard(shell_robo_shotcut_path, win_local_path)

if __name__ == '__main__':
    RunMain()
    
    print('Run auto test done!')
    pass