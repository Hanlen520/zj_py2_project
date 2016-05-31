# -*- coding: utf-8 -*-
'''
@author: zhengjin
'''

import os
import subprocess
import time
import FrameParse
import MemoryParse

def RobotiumTestSuiteRunner(testsuiteNames):
    for testrunner in testsuiteNames:
        cmd = "adb shell am instrument -w " + testrunner
        p = subprocess.Popen(cmd, shell=False)
        print("Test suite -> " + testrunner + " is running...")
        p.wait()
        time.sleep(2)

def PullTestDataFromAndroidStorage(localPath, androidPath):
    cmd = 'adb pull ' + androidPath + ' ' + localPath

    p = subprocess.Popen(cmd, shell=False)
    print('pull data from android external storage...')
    p.wait()
    time.sleep(2)

def ParseFramesLogFiles(localPath):
    frmLogFiles = []
    
    for fileName in os.listdir(localPath):
        if(fileName.startswith("Frames")):
            frmLogFiles.append(fileName)
        
    for logFile in frmLogFiles:
        print("Parse frames log file -> " + logFile)

        absInPath = os.path.join(localPath, logFile)
        absOutPath = os.path.join(localPath, logFile.split('.')[0] + "_parse.log")
        
        FrameParse.DoParseFrames(absInPath, absOutPath).ParseFrames()

def ParseMemLogFiles(localPath):
    MemLogFiles = []
    
    for fileName in os.listdir(localPath):
        if(fileName.startswith("MemSmaps")):
            MemLogFiles.append(fileName)
        
    for logFile in MemLogFiles:
        print("Parse memory log file -> " + logFile)

        absInPath = os.path.join(localPath, logFile)
        absOutPath = os.path.join(localPath, logFile.split('.')[0] + "_parse.log")
        MemoryParse.ParseMem(absInPath, absOutPath)


if __name__ == '__main__':
    flagRunTestSuite = False
    
    flagPullData = False
    flagPullCsvData = True
    
    flagRunTypeBoth = False
    flagRunTypeFrames = False
    flagRunTypeMemory = False
    
    testsuiteNames = []
    testsuiteNames.append("tv.fun.launcher.test/tv.fun.launcher.testrunner.LauncherFramesTestSuiteRunner")
#     testsuiteNames.append("tv.fun.launcher.test/.LauncherTestSuiteRunner")

    localPath = r"D:\Launcher_KeyTarget"
#     androidPath = "/sdcard/robotium/"  # for xiaomi
    androidPath = "/data/data/com.fun.tv/files/robotium/"   # for mele
    emmageePath = "/data/data/com.netease.qa.emmagee/files/"  # for tool emmagee

    if (flagRunTestSuite):
        try:
            RobotiumTestSuiteRunner(testsuiteNames)
        except Exception as ex:
            print("Exception: \n" + ex)
            exit()
    
    if (flagPullData):
        PullTestDataFromAndroidStorage(localPath, androidPath)
    if (flagPullCsvData):
        PullTestDataFromAndroidStorage(localPath, emmageePath)
    
    if (flagRunTypeBoth):
        ParseFramesLogFiles(localPath)
        ParseMemLogFiles(localPath)
    elif (flagRunTypeFrames):
        ParseFramesLogFiles(localPath)
    elif (flagRunTypeMemory): 
        ParseMemLogFiles(localPath)
    else:
        print("No parse exec!")
    
    print("Auto runner Done!")
    pass