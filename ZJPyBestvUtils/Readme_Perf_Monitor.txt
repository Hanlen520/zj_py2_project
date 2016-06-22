->
Memory

1. Get smaps virtual files: 
adb shell
ps | grep launcher  # get pid
cd /proc/pid
cat comm  # check app name
ll
su
cat smaps > /sdcard/smaps/smapsX  # generate map file
exit  # exit shell
adb pull /sdcard/smaps/ D:\  # get all files from "smaps" folder

2. Parse smaps file



->
Graphic frames

1. Update and override below file: 
E:\Git_Workspace\ottCocos\funTvCocosRc2\frameworks\js-bindings\cocos2d-x\cocos\base\CCDirector.cpp

void Director::showStats() {}
CCLOG("trace_frame: %f", _frameRate);  // print frames

2. Get the log for logcat: 
adb shell logcat -c && 
adb shell logcat -v time > D:\Launcher_Profile\framelogx.log



->
Exec the Robotium auto TCs to generate the log source file, 
and use the python scripts to parse the log files and generate the testing report.

Use the "LauncherBuild.py" to build the cocos based "Launcher" project.



->

