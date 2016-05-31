# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import shutil
import urllib2
import codecs

# --------------------------------------------------------------
# Vars
# --------------------------------------------------------------
sep = os.path.sep

workspace = "D:"

#ottcocos_debug_master
git_ottcocos_debug_master = workspace + sep + "ottcocos_debug_master" + sep + "ottCocos"

#funtv目录
funtv_workapace = git_ottcocos_debug_master + sep + "funTvCocosRc2"

#temp_apk目录
temp_apk= "F:" + sep + "temp_apk"

version = "1.0.0.56"

channel_code = {'vst':'2054',\
                'boyiletv':'2056',\
                'huan':'2079',\
                'tvapk':'2077',\
                'znds':'2055',\
                '7po':'2094',\
                'ijiatv':'2092',\
                'shafa':'2093',\
                '360tv':'2095',\
                'boxmate':'2052',\
                'herfans':'2097',\
                'wukongtv':'2096',\
                'tuzitv':'2102',\
                'alitv':'2103',\
                'zn8':'2130',\
                'guanfang':'2',\
                }

# --------------------------------------------------------------
# Functions
# --------------------------------------------------------------
def run_cmd(cmd):
    process = subprocess.Popen(cmd , shell = True, stdout=subprocess.PIPE)
    return process.stdout.read().strip()

def checkkeyword(filename,keyword):
    flag = False
    f = open(filename)
    try:
        for line in f.readlines():
            if keyword in line:
                print line.strip()
                flag = True
                break
    finally:
        f.close()
    return flag

def get_content(url):
    try:
        content_stream = urllib2.urlopen(url)
        content = content_stream.read()
        return content
    except urllib2.HTTPError, e:
        print "http error"
        print e.code
        exit()

# --------------------------------------------------------------
# Main
# --------------------------------------------------------------
if __name__=='__main__':
    reload(sys)
    sys.setdefaultencoding("utf-8")
    
    #检查日志开关
    a = funtv_workapace + sep + "frameworks" + sep + "runtime-src" + sep + "proj.android" + sep + "jni" + sep + "Application.mk"
    if(checkkeyword(a,"APP_CPPFLAGS += -DCOCOS2D_DEBUG=0 -DCOCOS_IDE=0") == False):
        print "检查日志开关错误"
        sys.exit();
    print "检查日志开关正确"
    
    #检查崩溃开关
    b = funtv_workapace + sep + "frameworks" + sep + "runtime-src" + sep + "proj.android" + sep + "src" + sep + "com" + sep + "cocos" + sep + "funtv" + sep + "FunApplication.java"
    if(checkkeyword(b,"public static boolean isRelease = true;") == False):
        print "检查崩溃开关错误"
        sys.exit();
    print "检查崩溃开关正确"
    
    #检查升级开关是否指向线上
    c = funtv_workapace + sep + "frameworks" + sep + "runtime-src" + sep + "proj.android" + sep + "src" + sep + "com" + sep + "fun" + sep + "tv" + sep + "utils" + sep + "updater" + sep + "UpdateChecker.java"
    if(checkkeyword(c,"final String channelUpgradeUrl = \"http://ott-api.fun.tv/ottauth-service/ott/api/index?version=") == False):
        print "检查武汉升级开关错误"
        sys.exit();
    print "检查武汉升级开关正确"
    
    if(checkkeyword(c,"final String updateUrl = \"http://update.funshion.com/interface/?object_id=18&v=") == False):
        print "检查北京升级开关错误"
        sys.exit();
    print "检查北京升级开关正确"
    
    #检查versioncode，versionname，channelcode
    d = funtv_workapace + sep + "frameworks" + sep + "runtime-src" + sep + "proj.android" + sep + "AndroidManifest.xml"
    print "检查versioncode，versionname，channelcode"
    checkkeyword(d,"android:versionCode")
    checkkeyword(d,"android:versionName")
    checkkeyword(d,"<meta-data android:name=\"channel_number\"")
    
    #检查HttpUrl.java文件中的相关地址是否会存在内网地址
    e = funtv_workapace + sep + "frameworks" + sep + "runtime-src" + sep + "proj.android" + sep + "src" + sep + "com" + sep + "webdata" + sep + "dataManager" + sep + "HttpUrl.java"
    if(checkkeyword(e,"172") == False):
        print "检查HttpUrl.java文件中的相关地址存在内网地址,请进一步检查"
        sys.exit();
    print "检查HttpUrl.java文件中的相关地址不存在内网地址"
    
    #生成homepage.json文件
    f = funtv_workapace + sep + "res" + sep + "homepage.json"
    if os.path.exists(f):
        os.remove(f)
    homepage_url = "http://ott-api.fun.tv/api/v3/index"
    homepage_url_result = get_content(homepage_url)
    fop = codecs.open(f, 'w', encoding='utf-8-sig')
    fop.write(homepage_url_result)
    fop.close()
    if os.path.exists(f) and os.path.getsize(f) > 0:
        print "homepage.json生成成功"
    else:
        print "homepage.json生成失败"
        sys.exit()

    sys.exit()
    #检查temp_apk目录
    if os.path.exists(temp_apk):
        shutil.rmtree(temp_apk)
    os.mkdir(temp_apk)
    os.makedirs(temp_apk + sep + version)
    

    for key in channel_code:
        print "-----------------------------------"
        print key + ":" + channel_code[key] + " compile start"
        
        print "清空publish目录"
        for parent,dirnames,filenames in os.walk(funtv_workapace + sep + "publish" + sep + "android"):
            for filename in filenames:
                os.remove(os.path.join(parent,filename))
        
        for parent,dirnames,filenames in os.walk(funtv_workapace + sep + "publish" + sep + "android"):
            if len(filenames) != 0:
                print "publish目录中生成apk失败"
                sys.exit()

        channel_code_path = temp_apk + sep + channel_code[key]
        os.makedirs(channel_code_path)

        fp = open(d)
    
        lines = fp.readlines()
        
        fp.close()
        
        output = open(d,"w")
        
        for line in lines:
            if not line:
                sys.exit()
            if "<meta-data android:name=\"channel_number\"" in line:
                print line
                temp = line.split("\"")
                if len(temp) == 5:
                    temp[3] = channel_code[key]
                    temp1 = temp[0] + "\"" + temp[1] + "\"" + temp[2] + "\"" + temp[3] + "\"" + temp[4]
                    output.write(temp[0] + "\"" + temp[1] + "\"" + temp[2] + "\"" + temp[3] + "\"" + temp[4])
                else:
                    sys.exit()
            else:
                output.write(line)
        output.close()
        
        os.chdir(funtv_workapace)
         
        result = run_cmd("cocos compile -p android --ap 20 -m release")
         
        if "BUILD SUCCESSFUL" in result:
            print "build success"
        else:
            print "build failed"
            sys.exit()
        
        #apk生成地址
        release_apk_file = funtv_workapace + sep + "publish" + sep + "android" + sep + "funTvCocos-release-signed.apk"
        if os.path.exists(release_apk_file):
            print "build apk success"
            new_name = "BesTV-" + version + "-for-" + key + ".apk"
            shutil.copyfile(release_apk_file,channel_code_path + sep + new_name)
            shutil.copyfile(channel_code_path + sep + new_name,temp_apk + sep + version + sep + new_name)
        else:
            print "build apk failed"
            sys.exit()
            
        #保留mapping文件
        mapping_file = funtv_workapace + sep + "frameworks" + sep + "runtime-src" + sep + "proj.android" + sep + "bin" + sep + "proguard" + sep + "mapping.txt"
        shutil.copyfile(mapping_file,channel_code_path + sep + "mapping.txt")
        print "保留mapping文件"
        
        #保留libcocos2djs.so文件
        ibcocos2djs_file = funtv_workapace + sep + "frameworks" + sep + "runtime-src" + sep + "proj.android" + sep + "obj" + sep + "local" + sep + "armeabi-v7a" + sep + "libcocos2djs.so"
        shutil.copyfile(ibcocos2djs_file,channel_code_path + sep + "libcocos2djs.so")
        print "保留libcocos2djs.so文件"
        
        print key + ":" + channel_code[key] + " compile over"
