# -*- coding: utf-8 -*-

'''
Created on 2016-7-18

@author: Vieira
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
g_city_list_file_name = 'Weather_city_list_test.txt'
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
    logging.info('Pass, %s.' %text)

def logging_failed(text, data):
    logging.error('Failed, %s.' %text)
    logging.error('Reason: %s', data)


# ------------------------------------------------
# Test case
# ------------------------------------------------
def test_weather_data_is_valid(req_parms):
    global g_total_failed

    resp = HttpJsonUtils.send_get_request_to_baidu_weather_service_and_return(req_parms)
    logging.debug(resp)
    json_arr = HttpJsonUtils.json_parse(resp)

    msg = 'verify the return code.'
    if (get_json_ret_num(json_arr)) == 0:
        logging_pass(msg)
    else:
        logging_failed(msg, ('Return code is %d' %get_json_ret_num(json_arr)))
        g_total_failed = g_total_failed + 1
        return

    msg = 'verify the return message.'
    if get_json_ret_msg(json_arr) == 'success':
        logging_pass(msg)
    else:
        logging_failed(msg, ('Return message is %s' %get_json_ret_msg(json_arr)))
        g_total_failed = g_total_failed + 1
        return

    today_weather = get_json_ret_data(json_arr)['today']
    cur_date = today_weather['date']
    msg = 'verify the current date from response.'
    if cur_date == time.strftime('%Y-%m-%d'):
        logging_pass(msg)
    else:
        logging_failed(msg, ('The current date is %s' %cur_date))
        g_total_failed = g_total_failed + 1
        return

    cur_temp = get_int_from_temp(today_weather['curTemp'])
    high_temp  = get_int_from_temp(today_weather['hightemp'])
    low_temp = get_int_from_temp(today_weather['lowtemp'])
    msg = 'verify the current temperature is valid.'
    if (cur_temp >= low_temp) and (cur_temp <= high_temp): 
        logging_pass(msg)
    else:
        logging_failed(msg, ('The current temperature is %d, high is %d, low is %d' %(cur_temp,high_temp,low_temp)))
        g_total_failed = g_total_failed + 1
        return


# ------------------------------------------------
# Help functions
# ------------------------------------------------
def get_int_from_temp(data):
    first = 0
    return re.findall(r'\d+', data)[first]

def get_json_ret_num(data):
    return data['errNum']

def get_json_ret_msg(data):
    return data['errMsg']

def get_json_ret_data(data):
    return data['retData']

def get_city_list():
    city_list_file_path = os.path.join(os.getcwd(), 'data', g_city_list_file_name)
    if not os.path.exists(city_list_file_path):
        logging.error('The city list file is NOT found.')
        exit(1)
    
    f = open(city_list_file_path, 'r')
    city_list = f.readlines()
    
    if len(city_list) == 0:
        logging.error('Read zero city item in the city list file.')
        exit(1)

    global g_total_num_of_city
    g_total_num_of_city = len(city_list)
    return city_list


# ------------------------------------------------
# Daemon thread
# ------------------------------------------------
def daemon_thread_main():
    #LOOP
    sleep_time = 30
    while True:
        logging.debug('*** Current, verify %d city of total %d.' %(g_cur_num_of_city, g_total_num_of_city))
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

    city_list = get_city_list()
    for city_item in city_list:
        tmp_list = city_item.strip().split(',')
        city_id = tmp_list[0]
        city_name = tmp_list[1]

        logging.info('---> START: test weather data for city id: %s, city name: %s' %(city_id,city_name))
        try:
            test_weather_data_is_valid({'cityid':str(city_id)})
        except Exception, e:
            logging.error('Error for city: %s' %city_id)
            logging.error('Exception: %s' %e)
        logging.info('---> END: test weather data for city id: %s, city name: %s\n' %(city_id,city_name))
        
        g_cur_num_of_city = g_cur_num_of_city + 1
        time.sleep(1)
    # end for

def main(fn):
    start = int(time.clock())
    fn()
    during = int(time.clock()) - start

    logging.info('The total number of cities is: %d' %g_total_num_of_city)
    logging.info('The failed number of cities is %d' %g_total_failed)
    logging.info('Verify baidu city weather data DONE, %s cost %d minutes %d seconds.' 
                 %(os.path.basename(__file__), (during/60), (during%60)))


if __name__ == '__main__':

    init_log_config()
    build_daemon_thread().start()
    main(test_main)

    logging.debug('Verify baidu weather service DONE.')
    pass
