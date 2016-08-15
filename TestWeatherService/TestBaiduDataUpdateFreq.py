# -*- coding: utf-8 -*-
'''
Created on 2016-8-8

@author: zhengjin

1. Collect baidu weather data for specified time.
2. Parse the collected weather data to show the data refresh frequency.

'''

import os
import time
import logging

from ZJPyUtils import HttpJsonUtils,FileUtils,WinSysUtils,LogUtils

# ----------------------------------------------------
# Variables
# ----------------------------------------------------
g_city_ids = ('101010100','101200101','101200105','101200601')  # 北京，武汉，江夏，黄石
g_log_dir = os.path.join(os.getcwd(),'logs','baidu_weather_data_update_freq')
g_cur_date = WinSysUtils.get_current_date()


# ----------------------------------------------------
# Collect weather data
# ----------------------------------------------------
def init_log():
    FileUtils.create_dir(g_log_dir)
    
    log_name = 'baidu_weather_data_update_freq_run_log_%s.log' %g_cur_date
    log_file = os.path.join(g_log_dir, log_name)
    LogUtils.init_log_config(logging.DEBUG, logging.INFO, log_file)

def send_reuqest_and_write_response():
    city_ids = g_city_ids
    url = 'http://apis.baidu.com/apistore/weatherservice/recentweathers'
    header_parms = {'apikey':'7705cca8df9fb3dbe696ce2310979a62'}

    file_name = 'baidu_weather_data_update_freq_src_%s.log' %g_cur_date
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


# ----------------------------------------------------
# Parse weather data
# ----------------------------------------------------
def create_weather_data_by_group(input_file_path, city_id):
    read_lines = FileUtils.read_file_and_ret_lines(input_file_path)
    if len(read_lines) == 0:
        print 'The lines count is 0 in file: %s' %input_file_path
        exit(1)
        
    split_word = ': '
    output_lines = []
    for line in read_lines:
        if line.find(split_word) < 0:
            continue
        json_data = HttpJsonUtils.json_parse(line.split(split_word)[1])
        if json_data['errNum'] != 0:
            continue
        tmp_city_id = json_data['retData']['cityid']
        if tmp_city_id == city_id:
#             output_lines.append(line.decode(FileUtils.CHARSET_UTF8))
            output_lines.append(line)
    # end for
    if len(output_lines) == 0:
        logging.warn('The weather data for city %s is none.' %city_id)
        exit(1)
        
    output_file_name = 'baidu_weather_data_update_freq_%s.log' %city_id
    output_file_path = os.path.join(g_log_dir, output_file_name)
#     FileUtils.write_lines_to_file(output_file_path,output_lines,flag_override=True,charset=FileUtils.CHARSET_UTF8)
    FileUtils.write_lines_to_file(output_file_path, output_lines)
    
    return output_file_path

def parse_weather_data_update_freq(file_path):
    changed_num = 0
    
    input_lines = FileUtils.read_file_and_ret_lines(file_path)
    lines_size = len(input_lines)
    if lines_size == 0:
        print 'The lines count is 0 in file %s' %file_path
        return

    output_lines = []
    output_lines.append('\n\n--------- Weather data changes log ---------\n')
    
    for i in xrange(0,(lines_size-1)):  # compare current record with next
        tmp_line_1 = input_lines[i]
        tmp_line_2 = input_lines[i + 1]
        tmp_items_1 = tmp_line_1.split(': ')
        tmp_items_2 = tmp_line_2.split(': ')
        tmp_json_data_1 = HttpJsonUtils.json_parse(tmp_items_1[1])
        tmp_json_data_2 = HttpJsonUtils.json_parse(tmp_items_2[1])
        tmp_lines_today = diff_today_weather_data(tmp_json_data_1, tmp_json_data_2)
        tmp_lines_forecast = diff_forecast_weather_data(tmp_json_data_1, tmp_json_data_2)

        if len(tmp_lines_today) > 0 or len(tmp_lines_forecast) > 0:
            changed_num += 1
            tmp_line = '\nThe weather data changed, %s to %s\n' %(tmp_items_1[0], tmp_items_2[0])
            output_lines.append(tmp_line)
        if len(tmp_lines_today) > 0:
            output_lines.append('<Today> data changed: \n')
            for line in tmp_lines_today:
                output_lines.append(line)
        if len(tmp_lines_forecast) > 0:
            output_lines.append('<Forecast> data changed: \n')  
            for line in tmp_lines_forecast:
                output_lines.append(line)
    # end for
    
    lines_summary = create_weather_data_summary(lines_size, changed_num)
    for line in lines_summary:
        output_lines.append(line)
    
    FileUtils.append_lines_to_file(file_path, output_lines)

def diff_today_weather_data(json_data_1, json_data_2):
    dic_data_1 = json_data_1['retData']['today']
    dic_data_2 = json_data_2['retData']['today']

    lines = []
    for key in dic_data_1.keys():
        if key == 'index':
            continue
        if dic_data_1[key] != dic_data_2[key]:
            tmp_line = 'The %s is changed from %s to %s\n' %(key,dic_data_1[key],dic_data_2[key])
            lines.append(tmp_line.encode(FileUtils.CHARSET_UTF8))
    return lines

def diff_forecast_weather_data(json_data_1, json_data_2):
    list_data_1 = json_data_1['retData']['forecast']
    list_data_2 = json_data_2['retData']['forecast']
    
    lines = []
    for i in xrange(0,len(list_data_1)):
        dic_data_1 = list_data_1[i]
        dic_data_2 = list_data_2[i]
        tmp_date = dic_data_1['date']
        for key in dic_data_1.keys():
            if dic_data_1[key] != dic_data_2[key]:
                tmp_line = 'Date %s: the %s is changed from %s to %s\n' %(tmp_date,key,dic_data_1[key],dic_data_2[key])
                lines.append(tmp_line.encode(FileUtils.CHARSET_UTF8))
    return lines

def create_weather_data_summary(total_num, changed_num):
    output_lines = []
    output_lines.append('\n--------- Weather data changes summary ---------\n')
    output_lines.append('The total number of records is: %d\n' %total_num)
    output_lines.append('The total number of weather data changed records is: %d\n' %changed_num)
    
    return output_lines


# ----------------------------------------------------
# Main
# ----------------------------------------------------
def main_collect_weather_data(during, interval):
    init_log()
    run_loop(during, interval)

def main_parse_weather_data(file_path):
    file_path_list = []
    for city_id in g_city_ids:
        tmp_path = create_weather_data_by_group(file_path, city_id)
        file_path_list.append(tmp_path)

    for path in file_path_list:
        parse_weather_data_update_freq(path)


if __name__ == '__main__':

    during = 24 * 60 * 60   # 12 hours
    interval = 5 * 60   # 5 minutes
    main_collect_weather_data(during, interval)
    
#     file_path = os.path.join(g_log_dir, 'baidu_weather_data_update_freq_src_20160815.log')
#     main_parse_weather_data(file_path)

    print '%s Done!' %(os.path.basename(__file__))
    pass