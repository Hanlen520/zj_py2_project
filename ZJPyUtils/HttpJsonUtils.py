# -*- coding: utf-8 -*-

'''
Created on 2016-7-18

@author: Vieira

Include the utils for send HTTP get and post requests, and parse JSON response.

'''

import urllib
import urllib2
import json
# import collections
import logging

# ----------------------------------------------------
# HTTP functions
# ----------------------------------------------------
def send_get_request_and_return(url, data, flag_urlencode=True):
    parms = None
    if flag_urlencode:
        parms = urllib.urlencode(data)
    else:
        parms = data

    resp = urllib.urlopen('%s?%s' %(url, parms))
    content = resp.read()
    
    if (content):
        return content
    else:
        logging.warn('The response data is null!')
        return ''

def send_get_request_with_header_and_return(url, header_parms, request_parms):
    parms = urllib.urlencode(request_parms)
    req = urllib2.Request('%s?%s' %(url, parms))
    for key,value in header_parms.items():
        req.add_header(key, value)

    resp = urllib2.urlopen(req)
    content = resp.read()
    if (content):
        return content
    else:
        logging.warn('The response request_parms from baidu service is null!')
        return ''

def send_post_request_and_return(url, data):
    print 'TODO: 2016-7-18'


# ----------------------------------------------------
# JSON functions
# ----------------------------------------------------
def json_parse(data):
#     json_arr = json.loads(data,object_pairs_hook=collections.OrderedDict)
    json_arr = json.loads(data)
    return json_arr

def get_json_ret_code(data):
    return data['retCode']

def get_json_ret_message(data):
    return data['retMsg']


# ----------------------------------------------------
# Main
# ----------------------------------------------------
def test_get_api():
    url = 'http://192.168.253.1:8887/weatherWebSite/testJsonDemo.php'
    req_parms = {'cityId':'101010100'}

    resp = send_get_request_and_return(url, req_parms)
    json_arr = json_parse(resp)
    print json_arr['data']['today']['curTemp']

def test_baidu_weather_api_without_key():
    url = 'http://apis.baidu.com/apistore/weatherservice/recentweathers'
    req_parms = {'cityId':'101010100'}

    resp = send_get_request_and_return(url, req_parms)
    print resp

def test_baidu_weather_api_with_key():
    url = 'http://apis.baidu.com/apistore/weatherservice/recentweathers'
    header_parms = {'apikey':'7705cca8df9fb3dbe696ce2310979a62'}
    req_parms = {'cityid':'101010100'}
    
    resp = send_get_request_with_header_and_return(url,header_parms,req_parms)
    print resp
    json_arr = json_parse(resp)
    print json_arr['retData']['today']['date']


if __name__ == '__main__':

#     test_get_api()
#     test_baidu_weather_api_without_key()
    test_baidu_weather_api_with_key()
    
    pass
