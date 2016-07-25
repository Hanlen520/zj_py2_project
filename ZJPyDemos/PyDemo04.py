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


# EXAMPLE 04
# import json
# 
# json_data = '{"total":239,"row":[{"code":"001","name":"\u4e2d\u56fd","addr":"Address 11","col4":"col4 data"},{"code":"002","name":"Name 2","addr":"Address 12","col4":"col4 data"}]}'
# json_arr = json.loads(json_data,encoding='utf-8')
# print json_arr['total']
# print json_arr['row'][0]['code']
# 
# for key in json_arr.keys():
#     print type(key)


# EXAMPLE 05
# str = u'test'
# print type(str)
# print type(str.encode('utf-8'))


# EXAMPLE 06
# import urllib2
# 
# url = 'http://apis.baidu.com/apistore/weatherservice/citylist?cityname=%E6%9C%9D%E9%98%B3'
# 
# req = urllib2.Request(url)
# req.add_header("apikey", "11c756e31e9bed863a743ccff784ddeb")
# 
# resp = urllib2.urlopen(req)
# content = resp.read()
# if(content):
#     print(content)
# else:
#     print 'Error.'


# EXAMPLE 07
# import re
#  
# str = '-28C'
# print re.findall(r'\d+', str)
# print re.findall(r'-(\d+)C', str)


# EXAMPLE 08
# city_id1 = 1
# city_name1 = 'city1'
# city_id2 = 2
# city_name2 = 'city2'
#  
# city_list = {}
# city_list[city_id1] = city_name1
# city_list[city_id2] = city_name2
#  
# for k,v in city_list.items():
#     print 'key: %s' %k
#     print 'value: %s' %v


# EXAMPLE 09
# dic = {'1':'a','3':'c','2':'b'}
# items = dic.items()
# items.sort()
# print items
# for k,v in items:
#     print k
#     print v
# 
# for k,v in sorted(dic.items(),key=lambda d:d[0]):
#     print k


# EXAMPLE 10
# i = 1
# i += 2
# print i


if __name__ == '__main__':

    print("%s done!" %os.path.basename(__file__))
    pass