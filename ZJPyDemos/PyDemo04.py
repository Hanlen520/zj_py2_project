# -*- coding: utf-8 -*-
'''
Created on 2016-7-13

@author: zhengjin
'''

import os

# EXAMPLE 01
# import platform
# system = platform.system()
# if system == 'Windows':
#     print 'Win'
# else:
#     print 'Linux'


# EXAMPLE 02
# if 'ANDROID_HOME' in os.environ:
#     print os.environ['ANDROID_HOME']


# EXAMPLE 03
# import time
# print time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))


if __name__ == '__main__':

    print("%s done!" %os.path.basename(__file__))
    pass