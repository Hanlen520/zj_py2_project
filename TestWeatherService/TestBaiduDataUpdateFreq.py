# -*- coding: utf-8 -*-
'''
Created on 2016-8-8

@author: zhengjin
'''

import os

from ZJPyUtils import HttpJsonUtils,FileUtils,WinSysUtils

def main():
    url = 'http://apis.baidu.com/apistore/weatherservice/recentweathers'
    header_parms = {'apikey':'7705cca8df9fb3dbe696ce2310979a62'}
    req_parms = {'cityid':'101010100'}
    resp = HttpJsonUtils.send_get_request_with_header_and_return(url,header_parms,req_parms)

    if resp is None:
        resp = 'null'

    file_name = 'baidu_weather_data_update_freq_%s.log' %WinSysUtils.get_current_date()
    file_path = os.path.join(os.getcwd(), 'logs', file_name)
    content = '%s: %s\n' %(WinSysUtils.get_current_date_and_time(), resp.decode('unicode_escape'))
    FileUtils.append_content_to_file(file_path, content, FileUtils.CHARSET_UTF8)

if __name__ == '__main__':

    main()
    print '%s Done!' %(os.path.basename(__file__))
    
    pass