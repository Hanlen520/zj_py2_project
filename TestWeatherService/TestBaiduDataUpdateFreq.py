# -*- coding: utf-8 -*-
'''
Created on 2016-8-8

@author: zhengjin
'''

import os
import time

from ZJPyUtils import HttpJsonUtils,FileUtils,WinSysUtils

# ----------------------------------------------------
# Functions
# ----------------------------------------------------
def send_reuqest_and_write_response():
    city_ids = ('101010100','101200101','101200105','101200601')  # 北京，武汉，江夏，黄石
    url = 'http://apis.baidu.com/apistore/weatherservice/recentweathers'
    header_parms = {'apikey':'7705cca8df9fb3dbe696ce2310979a62'}

    file_name = 'baidu_weather_data_update_freq_%s.log' %WinSysUtils.get_current_date()
    file_path = os.path.join(os.getcwd(),'logs','baidu_weather_data_update_freq',file_name)

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


# ----------------------------------------------------
# Main
# ----------------------------------------------------
def main(during, interval):
    start_time = time.clock()
    
    i = 1
    while ((int(time.clock()) - int(start_time)) < during):
        print 'Send request %d times.' %i
        send_reuqest_and_write_response()
        i += 1
        time.sleep(interval)


if __name__ == '__main__':

    during = 4 * 60 * 60  # 4 hour
    interval = 5 * 60  # 5 minutes
    main(during, interval)
    print '%s Done!' %(os.path.basename(__file__))
    
    pass