# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import shutil
import urllib2
import time
from datetime import g_cur_date
import xml.etree.ElementTree as ET
import re

# ------------------------------------------------
# Vars to be update
# ------------------------------------------------
prj_workspace = r"E:\Git_Workspace\ottCocos\funTvCocosRc2"
version_name = "1.0.0.64"
version_code = "20"
saved_apk_dir = r"D:\launcher_apk_builds"

channel_codes = {'vst':'2054',\
                'boyiletv':'2056',\
#                 'huan':'2079',\
#                 'tvapk':'2077',\
#                 'znds':'2055',\
#                 '7po':'2094',\
#                 'ijiatv':'2092',\
#                 'shafa':'2093',\
#                 '360tv':'2095',\
#                 'boxmate':'2052',\
#                 'herfans':'2097',\
#                 'wukongtv':'2096',\
#                 'tuzitv':'2102',\
#                 'alitv':'2103',\
#                 'zn8':'2130',\
#                 'guanfang':'2',\
                }

# ------------------------------------------------
# Helper methods
# ------------------------------------------------
def RunCommand(cmd):
    p = subprocess.Popen(cmd, shell=True)
    return p.wait()  # return code 0 -> success

def FindKeywordFromFile(file_path, key_word):
    flag = False

    if not os.path.isfile(file_path):
        print("The file %s is not found" %file_path)
        exit()
    
    f = open(file_path, "r")
    try:
        while(True):
            line = f.readline()
            if not line:
                break
            if((not FindCommentsTag(line)) and (key_word in line)):
                flag = True
                break
    finally:
        f.close()

    return flag

def ReadLinesFromFile(file_path):
    if not os.path.exists(file_path):
        print("The file %s is not found!" %file_path)
        exit()
    elif os.path.getsize(file_path) == 0:
        print("There is no content for file: %s" %file_path)
        exit()

    f = open(file_path, "r")
    lines = []
    try:
        lines = f.readlines()
    finally:
        f.close()
        
    return lines

# item = (name, str_old/ptn, str_new)
def ReplaceKeywordFromFile(file_path, lines, item):
    new_lines = ""
    for line in lines:
        if item[0] in line:
            new_lines += re.sub(item[1], item[2], line, count=1)  # use regex instead
            continue
        new_lines += line
    
    f = open(file_path, "w")
    try:
        f.write(new_lines)
    finally:
        f.close()

def FindCommentsTag(text):
    if(text.startswith(r"//") or text.strip().startswith(r"//")):
        return True
    else:
        return False

def CheckServer(url):
    try:
        content_stream = urllib2.urlopen(url)
        content = content_stream.read()
        return content
    except urllib2.HTTPError, e:
        print "http error: "
        print e.code

# ------------------------------------------------
# Check testing ENV
# ------------------------------------------------
def CheckDebugMode():
    file_path = os.path.join(prj_workspace, r"frameworks\runtime-src\proj.android\jni\Application.mk")
    verify_Word = "APP_CPPFLAGS += -DCOCOS2D_DEBUG=0 -DCOCOS_IDE=0"
    
    if FindKeywordFromFile(file_path, verify_Word):
        print("Application.mk, verify debug mode success!")
    else:    
        print("Application.mk, verify debug mode failed!")
        exit();

def CheckReleaseFlag():
    file_path = os.path.join(prj_workspace, r"frameworks\runtime-src\proj.android\src\com\cocos\funtv\FunApplication.java")
    verify_Word = "public static boolean isRelease = true;"
    
    if FindKeywordFromFile(file_path, verify_Word):
        print("FunApplication.java, verify isRelease success!")
    else:
        print("FunApplication.java, verify isRelease failed!")
        exit();
    
def CheckUpgradeChannels():
    file_path = os.path.join(prj_workspace, r"frameworks\runtime-src\proj.android\src\com\fun\tv\utils\updater\UpdateChecker.java")

    # check upgrade url for WH
    verify_Word = "final String channelUpgradeUrl = \"http://ott-api.fun.tv/ottauth-service/ott/api/index?version="
    if FindKeywordFromFile(file_path, verify_Word):
        print("UpdateChecker.java, verify var channelUpgradeUrl success!")
    else:
        print("UpdateChecker.java, verify var channelUpgradeUrl definition failed!")
        sys.exit();
    
    # check upgrade url for BJ
    verify_Word = "final String updateUrl = \"http://update.funshion.com/interface/?object_id=18&v="
    if FindKeywordFromFile(file_path, verify_Word):
        print("UpdateChecker.java, verify var updateUrl success!")
    else:
        print("UpdateChecker.java, verify var updateUrl failed!")
        sys.exit();

def CheckAndroidManifest():
    file_path = os.path.join(prj_workspace, r"frameworks\runtime-src\proj.android\AndroidManifest.xml")

    if(FindKeywordFromFile(file_path,"android:versionCode") and 
       FindKeywordFromFile(file_path,"android:versionName") and 
       FindKeywordFromFile(file_path,"android:name=\"channel_number\"")):
        print("AndroidManifest.xml, verify configs success!")
    else:
        ("AndroidManifest.xml, verify configs failed!")
        exit()
    
def CheckUrls():
    file_path = os.path.join(prj_workspace, r"frameworks\runtime-src\proj.android\src\com\webdata\dataManager\HttpUrl.java") 
    verify_Word = "sHomePageUrl = \"http://172.16.12.71/api/v3/index?mac=%s\""
    
    # check testing internal ip address is not exist or comment out
    if FindKeywordFromFile(file_path, verify_Word):
        print("HttpUrl.java, check url 172 failed!")
        sys.exit();
    else:
        print("HttpUrl.java, check url 172 success!")

def CheckHomepageConnect():
    file_path = os.path.join(prj_workspace, r"res\homepage.json")
    if os.path.exists(file_path):
        os.remove(file_path)

    homepage_url = "http://ott-api.fun.tv/api/v3/index"
    fop = open(file_path, 'w')
    try:
        fop.write(CheckServer(homepage_url))
    finally:
        fop.close()
    
    if(os.path.exists(file_path) and os.path.getsize(file_path) > 0):
        print("homepage.json, generate success!")
    else:
        print("homepage.json, generate failed!")
        sys.exit()

# ------------------------------------------------
# Process functions
# ------------------------------------------------
def ClearOldSavedApkDir(saved_build_dir):
    if os.path.exists(saved_apk_dir):
        shutil.rmtree(saved_apk_dir)
        time.sleep(2)  # wait for rmtree() done
        print("Clear old saved apk dirs success!")
    else:
        print("No old saved apk dirs found!")

def CreateSavedApkDir(saved_build_dir):
    os.makedirs(saved_build_dir)
    print("Create saved apk dirs success!")

def CreateSavedChannelDir(saved_apk_sub_dir):
    os.makedirs(saved_apk_sub_dir)
    print("Create channel dir success!")

def ClearOldPublishedApk():
    filepath = os.path.join(prj_workspace, r"publish\android")
    
    for parent,dirnames,filenames in os.walk(filepath):
        if len(filenames) > 0:
            for filename in filenames:
                if(filename.strip().endswith(".apk") or filename.strip().endswith(".APK")):
                    os.remove(os.path.join(parent, filename))
                    print("Clear old published apks success.")
        else:
            print("No old published apks found.")

def UpdateVersionCodeAndVersionName():
    file_path = os.path.join(prj_workspace, r"frameworks\runtime-src\proj.android\AndroidManifest.xml")
    names = ["versionCode", "versionName"]
    patns = ["\d{2}", "[0-9]\.[0-9]\.[0-9]\.\d{2}"]
    strs_new = [version_code, version_name]
    
    for i in range(0,2):
        ReplaceKeywordFromFile(file_path, ReadLinesFromFile(file_path), (names[i], patns[i], strs_new[i]))
    
    print("Version code and name is updated in AndroidManifest.xml success!")

def UpdateChannelNumber(channel_num):
    file_path = os.path.join(prj_workspace, r"frameworks\runtime-src\proj.android\AndroidManifest.xml")
    name = "channel_number"
#     str_old = ReadChannelNumberFromXml(file_path)
#     str_new = channel_num
    
    ReplaceKeywordFromFile(file_path, ReadLinesFromFile(file_path), (name, '\d{4}', channel_num), True)
    
    print("Channel number is updated in AndroidManifest.xml success!")
    
def ReadChannelNumberFromXml(file_path):
#     ET.register_namespace("android", "http://schemas.android.com/apk/res/android")
    tree = ET.parse(file_path)
     
    root = tree.getroot()
    nodelist = root.find("application").findall("meta-data")
    for node in nodelist:
        if(node.get("{http://schemas.android.com/apk/res/android}name") == "channel_number"):
            return node.get("{http://schemas.android.com/apk/res/android}value")

    print("The node channel_number is not found from AndroidManifest.xml!")
    exit()

def ExecBuildCommand(log_file_path, tag):
    print("************************************")
    print("* start to build apk for %s" %tag)
    print("************************************")
    
    os.chdir(prj_workspace)
    cmd = r"cocos compile -p android --ap 20 -m release -j4 >> %s" %log_file_path  # to be updated
    rc = RunCommand(cmd)
 
    AddFooterInLogFile(log_file_path, tag)
 
    if rc == 0:
        print("[Vieira] Run cocos command success!")
    else:
        print("[Vieira] Run cocos command failed!")
        exit()

def CreateLogFile(log_file):
    if os.path.exists(log_file):
        os.remove(log_file)

    f = open(log_file, "w")  # if not exist, create a new file
    try:
        f.write("***************** apk build log file ****************")
    finally:
        f.close()

def AddFooterInLogFile(log_file, tag):
    if not os.path.exists(log_file):
        print("The build log file is not found!")
        exit()
        
    lines = []
    lines.append("************************************\n")
    lines.append("* [Vieira] The build for %s is complete!\n" %tag)
    lines.append("************************************\n\n\n")
    
    f = open(log_file, "a")
    try:
        f.writelines(lines)
    finally:
        f.close()

def CopyAndRenameBuiltApk(saved_build_dir, saved_apk_sub_dir, channel):
    release_apk_path = os.path.join(prj_workspace, r"publish\android\funTvCocos-release-signed.apk")
    old_name = "funTvCocos-release-signed.apk"
    new_name = "BesTV-" + version_name + "-for-" + channel + ".apk"
 
    # When use shutil.copyfile(), raise no permission! Copy and rename here.
    if os.path.exists(release_apk_path):
        shutil.copy(release_apk_path, saved_build_dir)
        shutil.copy(release_apk_path, saved_apk_sub_dir)
        
        os.rename(os.path.join(saved_build_dir, old_name), os.path.join(saved_build_dir, new_name))
        os.rename(os.path.join(saved_apk_sub_dir, old_name), os.path.join(saved_apk_sub_dir, new_name))
        print("Copy and rename built apks success!")
    else:
        print("Built APK is not found!")
        exit()

def SaveMappingFile(channel, saved_apk_sub_dir):
    mapping_file = os.path.join(prj_workspace, r"frameworks\runtime-src\proj.android\bin\proguard\mapping.txt")
    old_mapping_name = "mapping.txt"
    new_mapping_name = "mapping-for-" + channel + ".txt"
    
    if not os.path.exists(mapping_file):
        print("The mapping file is not found!")
        exit()
    
    shutil.copy(mapping_file, saved_apk_sub_dir)
    os.rename(os.path.join(saved_apk_sub_dir, old_mapping_name), os.path.join(saved_apk_sub_dir, new_mapping_name))
    print("Save mapping file success!")
 
def SaveSoFile(saved_apk_sub_dir):
    ibcocos2djs_file = os.path.join(prj_workspace, r"frameworks\runtime-src\proj.android\obj\local\armeabi-v7a\libcocos2djs.so")
    
    if not os.path.exists(ibcocos2djs_file):
        print("The libcocos2djs.so file is not found!")
        exit()
    
    shutil.copy(ibcocos2djs_file, saved_apk_sub_dir)
    print("Save libcocos2djs.so file success!")

def CleanEnv():
    RestoreManifest()

def RestoreManifest():
    file_path = os.path.join(prj_workspace, r"frameworks\runtime-src\proj.android\AndroidManifest.xml")
    names = ["versionCode", "versionName", "channel_number"]
    patns = ["\d{2}", "[0-9]\.[0-9]\.[0-9]\.\d{2}","\d{4}"]
    strs_new = ['99', '1.0.0.99', '9999']
    
    for i in range(0,3):
        ReplaceKeywordFromFile(file_path, ReadLinesFromFile(file_path), (names[i], patns[i], strs_new[i]))

    print("Restore android Manifest.xml success!")


# ------------------------------------------------
# Main
# ------------------------------------------------
if __name__=='__main__':
#     reload(sys)
#     sys.setdefaultencoding("utf-8")
    
    # check env
    CheckDebugMode()
    CheckReleaseFlag()
#     CheckLogFromProguard()
    CheckUpgradeChannels()
    CheckAndroidManifest()
    CheckUrls()
    CheckHomepageConnect()

    
    # pre-conditions
    saved_build_dir = os.path.join(saved_apk_dir, version_name)
    ClearOldSavedApkDir(saved_build_dir)
    CreateSavedApkDir(saved_build_dir)
       
    log_file_path = os.path.join(saved_apk_dir, "build_log_%s" %g_cur_date.today())
    CreateLogFile(log_file_path)
  
    UpdateVersionCodeAndVersionName()
    
     
    # build for each channel number
    for key in channel_codes:
        saved_apk_sub_dir = os.path.join(saved_apk_dir, key + "_" + channel_codes[key])
      
        CreateSavedChannelDir(saved_apk_sub_dir)
        ClearOldPublishedApk()
        UpdateChannelNumber(channel_codes[key])
        
        ExecBuildCommand(log_file_path, "%s_%s" %(key, channel_codes.get(key)))
          
        CopyAndRenameBuiltApk(saved_build_dir, saved_apk_sub_dir, key)
        SaveMappingFile(key, saved_apk_sub_dir)
        SaveSoFile(saved_apk_sub_dir)
  
        print("%s -> %s, compile done!" %(key, channel_codes[key]))
    # end for


    # clear env
    CleanEnv()
    print("**** All build done!")
    
# end main