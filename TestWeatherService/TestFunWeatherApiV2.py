# -*- coding: utf-8 -*-
'''
Created on 2016-11-17

@author: zhengjin
'''

import os
import time
import logging

from ZJPyUtils import LogUtils
from ZJPyUtils import HttpJsonUtils
from ZJPyUtils import FileUtils
from ZJPyUtils import WinSysUtils

# ----------------------------------------------------
# Variables
# ----------------------------------------------------
g_const_fun_weather_api_url = 'http://172.17.12.110:8480/tv_message/weather2/city'
g_const_fun_weather_api_parm = 'plat_type=funtv&version=2.10.0.3_s&sid=FD5551A-SU&mac=28:76:CD:01:96:F6' + \
                '&random=1479353604311820&sign=fcc9a70567a644eda0201fbc9bc1ef15' + \
                '&province=&city=&area=&cityId=%s'

g_const_city_list_file_name = 'Weather_city_list_test.txt'
g_const_log_file_name = 'weather_api_v2_test_results_%s.log'

g_total_num_cities = 0
g_cities_failed = 0


# ----------------------------------------------------
# Log Functions
# ----------------------------------------------------
def log_env_setup():
    file_name = g_const_log_file_name % (time.strftime('%y-%m-%d_%H-%M-%S'))
    file_path = os.path.join(os.getcwd(), 'logs', file_name)
    LogUtils.init_log_config(logging.DEBUG, logging.INFO, file_path)

def log_report_header():
    logging.info('----------- START: get city weather data from API v2 -----------')

def log_report_trailer():
    logging.info('----------- Summary -----------')
    logging.info('Total number of cities: %d' % g_total_num_cities)
    logging.info('Total number of cities failed get data: %d' % g_cities_failed)
    logging.info('----------- END: get city weather data from API v2 -----------')


# ----------------------------------------------------
# Functions
# ----------------------------------------------------
def read_city_list():
    file_path = os.path.join(os.getcwd(), 'data', g_const_city_list_file_name)
    output_lines = FileUtils.read_file_and_ret_lines(file_path)
    if (len(output_lines) == 0):
        logging.error('No lines read from city list file!')
        exit(1)
    
    global g_total_num_cities
    g_total_num_cities = len(output_lines)
    return output_lines

def get_city_weather_data_from_api_v2(city_id):
    global g_cities_failed
    resp = ''
    try:
        resp = HttpJsonUtils.send_get_request_and_return(
            g_const_fun_weather_api_url, (g_const_fun_weather_api_parm % city_id), flag_urlencode=False)
    except Exception, e:
        logging.debug('Exception when request weather data for %s: %s' % (city_id, e))
        resp = 'Error send request'
        g_cities_failed += 1
        
    if (not is_response_json_type(resp)):
        resp = 'Invalid JSON type'
        g_cities_failed += 1
    if (not verify_ret_code_and_msg(HttpJsonUtils.json_parse(resp))):
        resp = 'Return code or message error'
        g_cities_failed += 1
        
    return resp

def is_response_json_type(resp):
    if resp == '': 
        logging.debug('The response data is null!')
        return False
    if not resp.startswith('{'):
        logging.debug('The content type of response is not JSON!')
        return False

    return True

def verify_ret_code_and_msg(resp_json):
    ret_code = int(resp_json['retCode'])
    if ret_code != 200:
        logging.debug('Response return code is NOT 200: %d' % ret_code)
        return False
    
    if resp_json['retMsg'] != 'ok':
        logging.debug('Response return message is NOT ok: %s' % resp_json['retMsg'])
        return False
    
    return True

def log_weather_data_line(input_line):
    items = input_line.split(',')
    city_id = items[0]
    city_name = items[1]
    logging.info('Get weather data for city: %s' % city_name)
    logging.info(get_city_weather_data_from_api_v2(city_id))


# ----------------------------------------------------
# Main
# ----------------------------------------------------
def main_get_city_weather_data():
    for line in read_city_list():
        WinSysUtils.exec_fun_and_log_exec_time(log_weather_data_line, line.rstrip('\n'))

def main_test_fun_weather_api():
    log_env_setup()
    log_report_header()
    WinSysUtils.exec_fun_and_log_exec_time(main_get_city_weather_data)
    log_report_trailer()


if __name__ == '__main__':

    main_test_fun_weather_api()
    logging.debug('%s Done!' % (os.path.basename(__file__)))

    pass
