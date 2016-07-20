->
Profile

1. Override below 2 files
E:\Git_Workspace\Launcher\funTvCocosRc2\frameworks\js-bindings\bindings\manual\ScriptingCore.cpp
E:\Git_Workspace\Launcher\funTvCocosRc2\frameworks\js-bindings\external\spidermonkey\prebuilt\android\armeabi-v7a\libjs_static.a

2. Compile and run
cocos run -p android --ap 20 -j4

3. Open launcher

4. Get the log from eclipse ide with filter "TRACE", or use adb command
adb shell logcat -c
adb shell logcat -v time > D:\Launcher_Profile\adblog.log

5. Parse the log to html format



->

