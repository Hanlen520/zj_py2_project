# -*- coding: utf-8 -*-
'''
@author: zhengjin
'''
#导入我们需要用到的包和类并且起别名  
import sys  
from com.android.monkeyrunner import MonkeyRunner as mr  
from com.android.monkeyrunner import MonkeyDevice as md  
from com.android.monkeyrunner import MonkeyImage as mi  

#connect device 连接设备  
#第一个参数为等待连接设备时间  
#第二个参数为具体连接的设备  
device = mr.waitForConnection(1.0,'172.17.5.15:5555')
if not device:
    print >> sys.stderr,"fail"  
    sys.exit(1)
#定义要启动的Activity
componentName='tv.fun.master/tv.fun.master.ui.activity.MainActivity'  
#启动特定的Activity  
device.startActivity(component=componentName)  
mr.sleep(3.0)  
#do someting 进行我们的操作  
#输入 helloworld  
# device.type('helloworld')  
#输入回车  
device.press('KEYCODE_ENTER')  
#return keyboard  
#device.press('KEYCODE_BACK')  
#------  
#takeSnapshot截图  
mr.sleep(10.0)  
result = device.takeSnapshot()  

#save to file 保存到文件  
result.writeToFile('d:\shot1.png','png');
