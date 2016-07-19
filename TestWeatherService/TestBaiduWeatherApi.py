# -*- coding: utf-8 -*-

'''
Created on 2016-7-18

@author: Vieira

Verify data from Baidu weather API for each city.
'''

import os
import time
import logging
import re
import threading

from ZJPyUtils import HttpJsonUtils

# ----------------------------------------------------
# Global variables
# ----------------------------------------------------
g_city_list_file_name = 'Weather_city_list.txt'
g_sleep_time_between_requests = 0.5


# ----------------------------------------------------
# Global constant variables
# ----------------------------------------------------
g_total_num_of_city = 0
g_cur_num_of_city = 0
g_total_failed = 0


# ------------------------------------------------
# Log functions
# ------------------------------------------------
def init_log_config():
    long_format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s'
    short_format = '%(filename)s: [%(levelname)s] >>> %(message)s'
    
    long_date_format = '%a, %d %b %Y %H:%M:%S'
    short_date_format = '%d %b %H:%M:%S'

    # log main handler
    logging.basicConfig(level=logging.DEBUG,format=short_format,datefmt=short_date_format)

    # set the file handler
    file_name = 'weather_service_test_%s.log' %(time.strftime('%y-%m-%d_%H-%M-%S'))
    file_path = os.path.join(os.getcwd(), 'logs', file_name)
    log_file = logging.FileHandler(filename=file_path,mode='w')
    log_file.setLevel(logging.INFO)
    log_file.setFormatter(logging.Formatter(fmt=long_format,datefmt=long_date_format))
    logging.getLogger('').addHandler(log_file)

def logging_pass(text):
    logging.info('Pass, %s' %text)

def logging_failed(text, reason):
    logging.error('Failed, %s' %text)
    logging.error('Reason: %s', reason)


# ------------------------------------------------
# Test case
# ------------------------------------------------
def test_weather_data_is_valid(req_parms):
    resp = HttpJsonUtils.send_get_request_to_baidu_weather_service_and_return(req_parms)
    if not verify_json_response_data(resp):
        test_failed_handler()
        return
    
    json_arr = HttpJsonUtils.json_parse(resp)
    if not verify_response_return_code(json_arr):
        test_failed_handler()
        return

    if not verify_response_return_message(json_arr):
        test_failed_handler()
        return
    
    if not verify_response_date(json_arr):
        test_failed_handler()
        return
    
    if not verify_response_temperature(json_arr):
        test_failed_handler()

def test_failed_handler():
    global g_total_failed
    g_total_failed = g_total_failed + 1

def verify_json_response_data(resp):
    if resp == '': 
        logging.error('The json response data is null!')
        return False
    
    if not resp.startswith('{'):
        logging.error('The response data content type is NOT json!')
        return False
    
    logging.info(resp)
    return True

def verify_response_return_code(json_arr):
    msg = 'verify the return code.'
    if (get_json_ret_num(json_arr)) == 0:
        logging_pass(msg)
        return True
    else:
        logging_failed(msg, ('Return code is %d' %get_json_ret_num(json_arr)))
        return False

def verify_response_return_message(json_arr):
    msg = 'verify the return message.'
    if get_json_ret_msg(json_arr) == 'success':
        logging_pass(msg)
        return True
    else:
        logging_failed(msg, ('Return message is %s' %get_json_ret_msg(json_arr)))
        return False

def verify_response_date(json_arr):
    msg = 'verify the current date from response.'
    
    today_weather = get_json_today_weather_data(json_arr)
    cur_date = today_weather['date']

    if cur_date == time.strftime('%Y-%m-%d'):
        logging_pass(msg)
        return True
    else:
        logging_failed(msg, ('The current date is %s' %cur_date))
        return False

def verify_response_temperature(json_arr):
    msg = 'verify the current temperature is valid.'
    
    today_weather = get_json_today_weather_data(json_arr)
    cur_temp = get_int_from_temp(today_weather['curTemp'])
    high_temp  = get_int_from_temp(today_weather['hightemp'])
    low_temp = get_int_from_temp(today_weather['lowtemp'])
    
    if (cur_temp >= low_temp) and (cur_temp <= high_temp): 
        logging_pass(msg)
        return True
    else:
        logging_failed(msg, ('The current temperature is %d, high is %d, low is %d' %(cur_temp,high_temp,low_temp)))
        return False


# ------------------------------------------------
# Help functions
# ------------------------------------------------
def get_int_from_temp(data):
    first_element = 0
    temp = re.findall(r'\d+', data)[first_element]
    return int(temp)

def get_json_ret_num(data):
    return data['errNum']

def get_json_ret_msg(data):
    return data['errMsg']

def get_json_ret_data(data):
    return data['retData']

def get_json_today_weather_data(data):
    return get_json_ret_data(data)['today']

def get_city_list():
    city_list_file_path = os.path.join(os.getcwd(), 'data', g_city_list_file_name)
    if not os.path.exists(city_list_file_path):
        logging.error('The city list file (%s) is NOT found!' %city_list_file_path)
        exit(1)
    
    f = open(city_list_file_path, 'r')
    city_list = f.readlines()
    
    if len(city_list) == 0:
        logging.error('Read zero city item in the city list file!')
        exit(1)

    global g_total_num_of_city
    g_total_num_of_city = len(city_list)

    return city_list


# ------------------------------------------------
# Daemon thread
# ------------------------------------------------
def daemon_thread_main():
    #LOOP
    sleep_time = 15
    while True:
        logging.debug('***** Current, verify %d city of total %d.' %(g_cur_num_of_city, g_total_num_of_city))
        time.sleep(sleep_time)

def build_daemon_thread():
    thread_name = 'baiduservicetest:daemon'
    t = threading.Thread(name=thread_name,target=daemon_thread_main)
    t.setDaemon(True)
    return t


# ------------------------------------------------
# Test main
# ------------------------------------------------
def test_main():
    global g_cur_num_of_city

    for city_item in get_city_list():
        tmp_list = city_item.strip().split(',')
        city_id = tmp_list[0]
        city_name = tmp_list[1]

        logging.info('---> START: verify weather data for city id: %s, city name: %s' %(city_id,city_name))
        try:
            test_weather_data_is_valid({'cityid':str(city_id)})
        except Exception, e:
            logging.error('Exception when verify city: %s (%s)' %(city_id,city_name))
            logging.error('Exception: %s' %e)
        logging.info('---> END: verify weather data for city id: %s, city name: %s\n' %(city_id,city_name))
        
        g_cur_num_of_city = g_cur_num_of_city + 1
        time.sleep(g_sleep_time_between_requests)
    # end for

def main(fn):
    start = int(time.clock())
    fn()
    during = int(time.clock()) - start

    logging.info('SUMMARY')
    logging.info('The total number of cities is: %d' %g_total_num_of_city)
    logging.info('The failed number of cities is %d' %g_total_failed)
    logging.info('Verify baidu city weather data DONE, %s cost %d minutes %d seconds.' 
                 %(os.path.basename(__file__), (during/60), (during%60)))
# end main


if __name__ == '__main__':

    init_log_config()
    build_daemon_thread().start()
    main(test_main)

    logging.debug('Verify baidu weather service DONE.')
    pass
