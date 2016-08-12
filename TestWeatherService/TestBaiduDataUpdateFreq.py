# -*- coding: utf-8 -*-
'''
Created on 2016-8-8

@author: zhengjin
'''

import os
import time
import logging

from ZJPyUtils import HttpJsonUtils,FileUtils,WinSysUtils,LogUtils

# ----------------------------------------------------
# Variables
# ----------------------------------------------------
g_log_dir = os.path.join(os.getcwd(),'logs','baidu_weather_data_update_freq')
g_cur_date = WinSysUtils.get_current_date()


# ----------------------------------------------------
# Functions
# ----------------------------------------------------
def init_log():
    FileUtils.create_dir(g_log_dir)
    
    log_name = 'baidu_weather_data_update_freq_run_log_%s.log' %g_cur_date
    log_file = os.path.join(g_log_dir, log_name)
    LogUtils.init_log_config(logging.DEBUG, logging.INFO, log_file)

def send_reuqest_and_write_response():
    city_ids = ('101010100','101200101','101200105','101200601')  # 北京，武汉，江夏，黄石
    url = 'http://apis.baidu.com/apistore/weatherservice/recentweathers'
    header_parms = {'apikey':'7705cca8df9fb3dbe696ce2310979a62'}

    file_name = 'baidu_weather_data_update_freq_%s.log' %g_cur_date
    file_path = os.path.join(g_log_dir, file_name)

    output_lines = []
    for id in city_ids:
        req_parms = {'cityid':id}
        resp = HttpJsonUtils.send_get_request_with_header_and_return(url,header_parms,req_parms)
        if resp is None:
            resp = 'null'

        line = '%s: %s\n' %(WinSysUtils.get_current_date_and_time(),resp.decode('unicode_escape'))
        output_lines.append(line) 
    # end for
    output_lines.append('\n')

    FileUtils.append_lines_to_file(file_path, output_lines, FileUtils.CHARSET_UTF8)

def print_cur_run_time(run_time):
    if run_time > 60:
        logging.info('Current run time: %d minutes, %d seconds' %(run_time/60, run_time%60))
    else:
        logging.info('Current run time: %d seconds' %(run_time%60))

def run_loop(during, interval):
    logging.info('----- START: test baidu weather data update frequency')

    start_time = time.clock()
    i = 1
#     while True:
    while 1:
        logging.info( 'Send request %d times.' %i)
        send_reuqest_and_write_response()
        i += 1
        
        run_time = int(time.clock()) - start_time
        print_cur_run_time(run_time)
        if run_time > during:
            break
        
        time.sleep(interval)
    # END LOOP
    logging.info('----- END: test baidu weather data update frequency')

def parse_weather_data():
    print 'TODO:'


# ----------------------------------------------------
# Main
# ----------------------------------------------------
if __name__ == '__main__':

    during = 2 * 60 * 60  # 2 hours
    interval = 5 * 60  # 5 minutes
    init_log()
    run_loop(during, interval)

    print '%s Done!' %(os.path.basename(__file__))
    pass