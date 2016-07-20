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
g_city_list_file_name = 'Weather_city_list_test.txt'
g_sleep_time_between_requests = 0.5
g_request_try_time = 3
g_flag_log_failed_connect_tcs = True


# ----------------------------------------------------
# Global constant variables
# ----------------------------------------------------
g_baidu_weather_service_url = 'http://apis.baidu.com/apistore/weatherservice/recentweathers'
g_baidu_service_request_header_parms = {'apikey':'7705cca8df9fb3dbe696ce2310979a62'}

g_total_num_of_city = 0
g_total_num_of_failed_connect = 0
g_total_num_of_failed_verification = 0
g_total_num_of_failed_verification_for_cur_temp = 0
g_cur_num_of_city = 0

g_num_of_city_retry_one_times_connect = 0
g_num_of_city_retry_two_times_connect = 0
g_num_of_city_retry_three_times_connect = 0

g_failed_connect_testcases = {}


# ------------------------------------------------
# Log functions
# ------------------------------------------------
def init_log_config(main_log_level, file_log_level, file_path):
    long_format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s'
    short_format = '%(filename)s: [%(levelname)s] >>> %(message)s'
    
    long_date_format = '%a, %d %b %Y %H:%M:%S'
    short_date_format = '%d %b %H:%M:%S'

    # log main handler
    logging.basicConfig(level=main_log_level,format=short_format,datefmt=short_date_format)

    # set the file handler
    log_file = logging.FileHandler(filename=file_path, mode='w')
    log_file.setLevel(file_log_level)
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
def test_weather_data_is_valid(city_id, city_name):
    global g_num_of_city_retry_one_times_connect
    global g_num_of_city_retry_two_times_connect
    global g_num_of_city_retry_three_times_connect
    global g_total_num_of_failed_connect
    global g_failed_connect_testcases

    resp = None
    json_arr = None
    flag_connect_validate = False
    for i in range(1,(g_request_try_time + 1)):
        logging.debug('Try to send request to Baidu weather API for %d times.' %i)
        try:
            resp = HttpJsonUtils.send_get_request_with_header_and_return(
                g_baidu_weather_service_url, g_baidu_service_request_header_parms, {'cityid':str(city_id)})
            json_arr = HttpJsonUtils.json_parse(resp)
        except Exception, e:
            logging.error('Exception: %s' %e)

        if verify_response_content_type_json(resp) and verify_response_return_code(json_arr):
            flag_connect_validate = True
            if i == 1:
                g_num_of_city_retry_one_times_connect = g_num_of_city_retry_one_times_connect + 1
            elif i == 2:
                g_num_of_city_retry_two_times_connect = g_num_of_city_retry_two_times_connect + 1
            elif i == 3:
                g_num_of_city_retry_three_times_connect = g_num_of_city_retry_three_times_connect + 1
            else:
                logging.fatal('Unexpected connect retry times.')
            break
        time.sleep(g_sleep_time_between_requests)
    # end for
    
    if not flag_connect_validate:
        g_total_num_of_failed_connect = g_total_num_of_failed_connect + 1
        if g_flag_log_failed_connect_tcs:
            g_failed_connect_testcases[str(city_id)] = city_name
        return
    
    verify_response_data(json_arr)
# end

def verify_response_data(json_arr):
    global g_total_num_of_failed_verification_for_cur_temp

    try:
        if not verify_response_return_message(json_arr):
            test_failed_handler()
            return
        if not verify_response_cur_date(json_arr):
            test_failed_handler()
            return
        if not verify_response_temperature(json_arr):
            # cur_temperature failed is not added into total failed
            g_total_num_of_failed_verification_for_cur_temp = g_total_num_of_failed_verification_for_cur_temp + 1
    except Exception, e:
        logging.error('Exception: %s' %e)
        test_failed_handler()

def test_failed_handler():
    global g_total_num_of_failed_verification
    g_total_num_of_failed_verification = g_total_num_of_failed_verification + 1

def verify_response_content_type_json(resp):
    if resp == '': 
        logging.error('The json response data is null!')
        return False
    if not resp.startswith('{'):
        logging.error('The content type of response is not JSON!')
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

def verify_response_cur_date(json_arr):
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
        time.sleep(sleep_time)
        logging.debug('***** Current, verify %d city of total %d.' %(g_cur_num_of_city, g_total_num_of_city))

def build_daemon_thread():
    thread_name = 'baiduservicetest:daemon'
    t = threading.Thread(name=thread_name,target=daemon_thread_main)
    t.setDaemon(True)
    return t


# ------------------------------------------------
# Test main
# ------------------------------------------------
def setup_main():
    file_name = 'weather_service_test_%s.log' %(time.strftime('%y-%m-%d_%H-%M-%S'))
    file_path = os.path.join(os.getcwd(), 'logs', file_name)
    init_log_config(logging.DEBUG, logging.INFO, file_path)
    
    build_daemon_thread().start()

def test_main():
    global g_cur_num_of_city

    for city_item in get_city_list():
        tmp_list = city_item.strip().split(',')
        city_id = tmp_list[0]
        city_name = tmp_list[1]

        logging.info('---> START: verify weather data for city id: %s, city name: %s' %(city_id,city_name))
        test_weather_data_is_valid(city_id, city_name)
        logging.info('---> END: verify weather data for city id: %s, city name: %s\n' %(city_id,city_name))
        
        g_cur_num_of_city = g_cur_num_of_city + 1
        time.sleep(g_sleep_time_between_requests)
    # end for

def main(fn):
    start = int(time.clock())
    fn()
    during = int(time.clock()) - start
    
    logging_summary()
    logging.info('Verify baidu city weather data DONE, %s cost %d minutes %d seconds.\n' 
                 %(os.path.basename(__file__), (during/60), (during%60)))

    if (len(g_failed_connect_testcases) > 0):
        log_failed_connect_cities()

def logging_summary():
    logging.info('SUMMARY')
    logging.info('The total number of cities is: %d' %g_total_num_of_city)
    
    logging.info('The total number of pass is: %d' 
                 %(g_total_num_of_city - g_total_num_of_failed_connect - g_total_num_of_failed_verification))
    logging.info('The number of cities retry 1 times connect is: %d' %g_num_of_city_retry_one_times_connect)
    logging.info('The number of cities retry 2 times connect is: %d' %g_num_of_city_retry_two_times_connect)
    logging.info('The number of cities retry 3 times connect is: %d' %g_num_of_city_retry_three_times_connect)
    
    logging.info('The number of failed connect is： %d' %g_total_num_of_failed_connect)
    logging.info('The number of failed verification is： %d' %g_total_num_of_failed_verification)
    logging.info('The number of failed verification for current temperature is： %d\n' 
                 %g_total_num_of_failed_verification_for_cur_temp)
    
def log_failed_connect_cities():
    logging.info('Failed connect cities: id,name')
    for k,v in g_failed_connect_testcases.items():
        logging.info('%s,%s' %(str(k), v))


if __name__ == '__main__':

    setup_main()
    main(test_main)

    logging.debug('Verify baidu weather service DONE.')
    pass
