# -*- coding: utf-8 -*-

'''
Created on 2016-7-19

@author: Vieira

Verify the weather data from Funshion service is consistent with Baidu.
'''

import os
import time
import logging

from ZJPyUtils import HttpJsonUtils

# ----------------------------------------------------
# Global variables
# ----------------------------------------------------
g_city_list_file_name = 'Weather_city_list_test.txt'
g_request_try_time = 3
g_sleep_time_between_requests = 0.5


# ----------------------------------------------------
# Global constant variables
# ----------------------------------------------------
g_baidu_weather_service_url = 'http://apis.baidu.com/apistore/weatherservice/recentweathers'
g_baidu_service_request_header_parms = {'apikey':'7705cca8df9fb3dbe696ce2310979a62'}

g_fun_weather_service_url = 'http://card.tv.funshion.com/weather/city'
g_fun_weather_service_parms = 'plat_type=funtv&version=2.6.0.11_s&sid=FD5551A-SU&mac=28:76:CD:01:96:F6&' + \
                            'random=1468389831575632&sign=a3e7422bef887d61a518ac64e3e234fa&cityId=101320101'


# ----------------------------------------------------
# Http functions
# ----------------------------------------------------
def get_city_weather_data_from_baidu_service(city_id):
    for i in range(1,(g_request_try_time + 1)):
        logging.debug('Try to send request to Baidu weather API for %d times.' %i)
        resp = HttpJsonUtils.send_get_request_with_header_and_return(
            g_baidu_weather_service_url, g_baidu_service_request_header_parms, {'cityid':str(city_id)})
        
        if verify_response_content_type_json(resp):
            json_arr = HttpJsonUtils.json_parse(resp)
            if verify_response_return_code_and_msg(json_arr):
                return json_arr
        time.sleep(g_sleep_time_between_requests)
    # end for
    return ''

def get_city_weather_data_from_fun_service(city_id):
    for i in range(1,(g_request_try_time + 1)):
        logging.debug('Try to send request to fun weather API for %d times.' %i)
        resp = HttpJsonUtils.send_get_request_and_return(
                g_fun_weather_service_url, g_fun_weather_service_parms, flag_urlencode=False)         

        if verify_response_content_type_json(resp):
            json_arr = HttpJsonUtils.json_parse(resp)
            if verify_response_return_code_and_msg(json_arr):
                return json_arr
        time.sleep(g_sleep_time_between_requests)
    #end for
    return ''

def verify_response_content_type_json(resp):
    if resp == '': 
        logging.error('The response data is null!')
        return False
    if not resp.startswith('{'):
        logging.error('The content type of response is not JSON!')
        return False
    
    logging.info(resp)
    return True

def verify_response_return_code_and_msg(json_arr):
    if (get_response_ret_num(json_arr)) == 0:
        return True
    else:
        logging.error(('Response return code is %d' %get_response_ret_num(json_arr)))
        return False
     
    if get_response_ret_msg(json_arr) == 'success':
        return True
    else:
        logging.error('Response return message is %s' %get_response_ret_msg(json_arr))
        return False

def get_response_ret_num(data):
    return data['errNum']

def get_response_ret_msg(data):
    return data['errMsg']

def get_response_ret_data(data):
    return data['retData']


# ----------------------------------------------------
# Verification
# ----------------------------------------------------
def verify_main():
    
    for city_item in get_city_list():
        fields = city_item.strip().split(',')
        city_id = fields[0]
        city_name = fields[1]

        resp_json_baidu = get_city_weather_data_from_baidu_service(city_id)
        resp_json_fun = get_city_weather_data_from_fun_service(city_id)
        logging.info('---> START: verify weather data for city id: %s, city name: %s' %(city_id,city_name))
        verify_resp_today_weather_data(resp_json_baidu, resp_json_fun)
        logging.info('---> END: verify weather data for city id: %s, city name: %s\n' %(city_id,city_name))

def verify_resp_today_weather_data(json_src, json_target):
    print 'TODO:'
    
def verify_resp_forecast_weather_data(json_src, json_target):
    print 'TODO:'
    
def get_city_list():
    city_list_file_path = os.path.join(os.getcwd(), 'data', g_city_list_file_name)
    if not os.path.exists(city_list_file_path):
        logging.error('The city list file (%s) is NOT found!' %city_list_file_path)
        exit(1)
    
    f = open(city_list_file_path, 'r')
    city_list = f.readlines()
    if len(city_list) == 0:
        logging.error('Read 0 city item in the city list file!')
        exit(1)

    global g_total_num_of_city
    g_total_num_of_city = len(city_list)

    return city_list


# ----------------------------------------------------
# Main
# ----------------------------------------------------

if __name__ == '__main__':
    
    print 'Done!'
    pass