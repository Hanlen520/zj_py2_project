# -*- coding: utf-8 -*-

'''
Created on 2016-7-18

@author: Vieira

Include the utils for http post and get request, and parse json response data.

'''

import urllib
import urllib2
import json
# import collections
import logging

# ----------------------------------------------------
# Global variables
# ----------------------------------------------------
g_baidu_weather_service_url = 'http://apis.baidu.com/apistore/weatherservice/recentweathers'
g_baidu_weather_service_api_key = '7705cca8df9fb3dbe696ce2310979a62'


# ----------------------------------------------------
# HTTP functions
# ----------------------------------------------------
def send_get_request_and_return(url, data):
    parms = urllib.urlencode(data)
    resp = urllib.urlopen('%s?%s' %(url, parms))
    content = resp.read()
    
    if (content):
        return content
    else:
        logging.warn('The response data is null!')
        return ''

def send_post_request_and_return(url, data):
    print 'TODO:'

def send_get_request_to_baidu_weather_service_and_return(data):
    parms = urllib.urlencode(data)
    req = urllib2.Request('%s?%s' %(g_baidu_weather_service_url, parms))
    req.add_header('apikey', g_baidu_weather_service_api_key)

    resp = urllib2.urlopen(req)
    content = resp.read()
    if (content):
        return content
    else:
        logging.warn('The response data from baidu service is null!')
        return ''


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

def test_baidu_weather_api():
    req_parms = {'cityid':'101010100'}
    resp = send_get_request_to_baidu_weather_service_and_return(req_parms)
    logging.debug(resp)
    json_arr = json_parse(resp)
    print json_arr['retData']['today']['date']


if __name__ == '__main__':

#     test_get_api()
    test_baidu_weather_api()
    pass
