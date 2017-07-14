# -*- coding: utf-8 -*-

'''
Created on 2016-7-19

@author: Vieira

Verify the city weather data from Funshion API.
1) get data success
2) data is consistent with Baidu service
'''

import os
import time
import logging

from ZJPyUtils import HttpJsonUtils

# ----------------------------------------------------
# Global variables
# ----------------------------------------------------
g_baidu_weather_service_url = 'http://apis.baidu.com/apistore/weatherservice/recentweathers'
g_baidu_service_request_header_parms = {'apikey':'7705cca8df9fb3dbe696ce2310979a62'}

g_fun_weather_service_url = 'http://card.tv.funshion.com/weather/city'
g_fun_weather_service_parms = 'mac=28:76:CD:01:96:F6&random=1468389831575632' + \
                            '&sign=a3e7422bef887d61a518ac64e3e234fa&cityId=%s'

g_city_list_file_name = 'Weather_city_list_compare.txt'

g_request_try_time = 3
g_sleep_time_between_requests = 0.5

g_tag_baidu = 'Baidu'
g_tag_funshion = 'Funshion'

# summary fields
g_total_num_of_cities = 0
g_total_failed_num_of_cities = 0

g_failed_cities = {}


# ------------------------------------------------
# Helper functions
# ------------------------------------------------
def init_log_config(main_log_level, file_log_level, file_path):
    long_format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s'
    short_format = '%(filename)s: [%(levelname)s] >>> %(message)s'
    
    long_date_format = '%a, %d %b %Y %H:%M:%S'
    short_date_format = '%d %b %H:%M:%S'

    # log main handler
    logging.basicConfig(level=main_log_level, format=short_format, datefmt=short_date_format)

    # set the file handler
    log_file = logging.FileHandler(filename=file_path, mode='w')
    log_file.setLevel(file_log_level)
    log_file.setFormatter(logging.Formatter(fmt=long_format, datefmt=long_date_format))
    logging.getLogger('').addHandler(log_file)

def get_city_list():
    city_list_file_path = os.path.join(os.getcwd(), 'data', g_city_list_file_name)
    if not os.path.exists(city_list_file_path):
        logging.error('The city list file (%s) is NOT found!' % city_list_file_path)
        exit(1)
    
    city_list = []
    f = open(city_list_file_path, 'r')
    try:
        city_list = f.readlines()
    except Exception, e:
        logging.error('Exception: %s' % e)
        logging.error('Exception when read lines from city list file.')
        exit(1)
    finally:
        f.close()

    if len(city_list) == 0:
        logging.error('Read 0 city item in the city list file!')
        exit(1)

    global g_total_num_of_cities
    g_total_num_of_cities = len(city_list)

    return city_list


# ----------------------------------------------------
# Http functions
# ----------------------------------------------------
def get_city_weather_data_from_baidu_service(city_id):
    for i in range(1, (g_request_try_time + 1)):
        logging.debug('Try to send request to Baidu weather API for %d times.' % i)
        
        resp = ''
        try:
            resp = HttpJsonUtils.send_get_request_with_header_and_return(
                g_baidu_weather_service_url, g_baidu_service_request_header_parms, {'cityid':str(city_id)})
        except Exception, e:
            logging.error('Exception when send request to Baidu weather service.')
            logging.error('Exception: %s' % e)

        if verify_response_content_type_json(g_tag_baidu, resp):
            json_arr = HttpJsonUtils.json_parse(resp)
            if verify_resp_ret_code_and_msg_for_baidu(json_arr):
                return json_arr
        time.sleep(g_sleep_time_between_requests)
    # end for
    
    return ''

def get_city_weather_data_from_fun_service(city_id):
    for i in range(1, (g_request_try_time + 1)):
        logging.debug('Try to send request to fun weather API for %d times.' % i)

        resp = ''        
        try:
            resp = HttpJsonUtils.send_get_request_and_return(
                    g_fun_weather_service_url, (g_fun_weather_service_parms % city_id), flag_urlencode=False)
        except Exception, e:
            logging.error('Exception when send request to Funshion weather service.')
            logging.error('Exception: %s' % e)

        if verify_response_content_type_json(g_tag_funshion, resp):
            json_arr = HttpJsonUtils.json_parse(resp)
            if verify_resp_ret_code_and_msg_for_fun(json_arr):
                return json_arr
        time.sleep(g_sleep_time_between_requests)
    # end for

    return ''

def verify_response_content_type_json(tag, resp):
    if resp == '': 
        logging.warn('The response data is null!')
        return False
    if not resp.startswith('{'):
        logging.warn('The content type of response is not JSON!')
        return False

    if tag == g_tag_baidu:
        resp = resp.decode('unicode_escape')  # convert unicode '\u5317\u4eac' to Chinese word

    logging.info('%s: %s' % (tag, resp))
    return True

def verify_resp_ret_code_and_msg_for_baidu(json_arr):
    if json_arr['errNum'] == 0:
        if json_arr['errMsg'] == 'success':
            return True
        else:
            logging.warn('Response return message is %s' % json_arr['errMsg'])
            return False
    else:
        logging.warn('Response return code is %d' % json_arr['errNum'])
        return False
     
def verify_resp_ret_code_and_msg_for_fun(json_arr):
    ret_code = int(json_arr['retCode'])  # str to int
    if ret_code == 200:
        if json_arr['retMsg'] == 'ok':
            return True
        else:
            logging.warn('Response return message is %s' % json_arr['retMsg'])
            return False
    else:
        logging.warn('Response return code is %d' % ret_code)
        return False


# ----------------------------------------------------
# Verification
# ----------------------------------------------------
def verify_main():
    global g_total_num_of_cities
    
    for city_item in get_city_list():
        city_item = city_item.strip().rstrip('\n')
        fields = city_item.split(',')
        if len(fields) != 2:
            logging.warn('Invalid city item: %s\n' % city_item)
            if g_total_num_of_cities > 1:
                g_total_num_of_cities -= 1
            continue
            
        city_id = fields[0]
        city_name = fields[1]

        logging.info('---> START: compare weather data for city id: %s, city name: %s' % (city_id, city_name))
        resp_json_baidu = get_city_weather_data_from_baidu_service(city_id)
        resp_json_fun = get_city_weather_data_from_fun_service(city_id)

        if resp_json_baidu == '':
            logging.error('The response json from Baidu service is null.')
            verify_failed_handler(city_id, city_name)
            continue
        if resp_json_fun == '':
            logging.error('The response json from Funshion service is null.')
            verify_failed_handler(city_id, city_name)
            continue

        verify_today = verify_today_weather_data(resp_json_baidu, resp_json_fun)
        verify_forecast = verify_forecast_weather_data(resp_json_baidu, resp_json_fun)
        if (not verify_today) or (not verify_forecast):
            verify_failed_handler(city_id, city_name)
        logging.info('---> END: compare weather data for city id: %s, city name: %s\n' % (city_id, city_name))
    # end for

def verify_failed_handler(city_id, city_name):
    global g_total_failed_num_of_cities
    global g_failed_cities
    
    g_total_failed_num_of_cities += 1
    g_failed_cities[city_id] = city_name

def verify_today_weather_data(resp_json_baidu, resp_json_fun):
    logging.info('TODAY: weather data verification')
    try:
        if verify_resp_today_weather_data(
                get_today_weather_data_for_baidu(resp_json_baidu), get_today_weather_data_for_fun(resp_json_fun)):
            logging.info('TODAY: the weather data is equal for Baidu and Fun.')
            return True
        else:
            logging.error('TODAY: the weather data is NOT equal for Baidu and Fun.')
            return False
    except Exception, e:
        logging.error('Exception: %s' % e)
        logging.error('TODAY: exception when verify weather data for Baidu and Fun.')
        return False

def verify_forecast_weather_data(resp_json_baidu, resp_json_fun):
    logging.info('FORECAST: weather data verification')
    try:
        if verify_resp_forecast_weather_data(
                get_forecast_weather_data_for_baidu(resp_json_baidu), get_forecast_weather_data_for_fun(resp_json_fun)):
            logging.info('FORECAST: the weather data is equal for Baidu and Fun.')
            return True
        else:
            logging.error('FORECAST: the weather data is NOT equal for Baidu and Fun.')
            return False
    except Exception, e:
        logging.error('Exception: %s' % e)
        logging.error('FORECAST: exception when verify weather data for Baidu and Fun.')
        return False

def verify_resp_today_weather_data(json_baidu, json_fun):
    ret = True
    for key in json_baidu.keys():
        if key == 'index':  # skip verify data for key "index"
            continue
        if not json_baidu[key] == json_fun[key]:
            logging.error('Today values are different. Key: %s, Baidu value: %s, Fun value: %s' 
                          % (key, json_baidu[key], json_fun[key]))
            ret = False
    # end for
    return ret
    
def verify_resp_forecast_weather_data(json_baidu, json_fun):
    if not len(json_baidu) == len(json_fun):
        logging.error('The days of forecast is NOT equal for Baidu and Funshion.')
        return False
    
    ret = True
    for i in range(0, len(json_baidu)):
        if not verify_day_weather_data_in_forecast(json_baidu[i], json_fun[i]):
            ret = False
    return ret

def verify_day_weather_data_in_forecast(json_baidu, json_fun):
    logging.info('Verify forecast weather data at %s.' % json_baidu['date'])
    
    ret = True
    for key in json_baidu.keys():
        if not json_baidu[key] == json_fun[key]:
            logging.error('Forecast values are different. Key: %s, Baidu value: %s, Fun value: %s' 
                          % (key, json_baidu[key], json_fun[key]))
            ret = False
    # end for
    return ret
    
def get_today_weather_data_for_baidu(json_data):
    return json_data['retData']['today']

def get_today_weather_data_for_fun(json_data):
    return json_data['data']['today']

def get_forecast_weather_data_for_baidu(json_data):
    return json_data['retData']['forecast']

def get_forecast_weather_data_for_fun(json_data):
    return json_data['data']['forecast']


# ----------------------------------------------------
# Main
# ----------------------------------------------------
def main_setup():
    file_name = 'weather_data_compare_results_%s.log' % (time.strftime('%y-%m-%d_%H-%M-%S'))
    file_path = os.path.join(os.getcwd(), 'logs', file_name)
    init_log_config(logging.DEBUG, logging.INFO, file_path)
    
def main(fn):
    start = int(time.clock())
    fn()
    during = int(time.clock()) - start
    
    log_verification_summary()
    log_failed_cities()
    log_execution_time(during)

def log_execution_time(during):
    logging.info('Compare weather data for Baidu and Funshion DONE, %s cost %d minutes %d seconds.\n' 
                 % (os.path.basename(__file__), (during / 60), (during % 60)))

def log_verification_summary():
    logging.info('SUMMARY')
    logging.info('The total number of verification cities is: %d' % g_total_num_of_cities)
    logging.info('The total number of pass verification cities is: %d' 
                 % (g_total_num_of_cities - g_total_failed_num_of_cities))
    logging.info('The total number of failed verification cities is: %d\n' % g_total_failed_num_of_cities)

def log_failed_cities():
    if len(g_failed_cities) > 0:
        logging.info('Failed verification cities: id,name')
        for k, v in sorted(g_failed_cities.items(), key=lambda f:f[0]):  # sorted by key
            logging.info('%s,%s' % (str(k), v))
    logging.info('')


if __name__ == '__main__':
    
    main_setup()
    main(verify_main)
    
    logging.debug('%s Done!' % (os.path.basename(__file__)))
