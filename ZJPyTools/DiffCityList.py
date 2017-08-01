# -*- coding: utf-8 -*-

'''
Created on 2016-7-26

@author: zhengjin

Show the gaps of cities list between local and official.

'''
import os
import logging

from ZJPyUtils import FileUtils
from ZJPyUtils import LogUtils

# ----------------------------------------------------
# Global variables
# ----------------------------------------------------
g_list_of_city_ids_not_match = {}
g_list_of_city_names_not_match = {}


# ----------------------------------------------------
# Main functions
# ----------------------------------------------------
def diff_main():
    global g_list_of_city_ids_not_match
    global g_list_of_city_names_not_match
    
    data_dir = os.path.join(os.getcwd(), 'data')
    lines_src_local = FileUtils.read_file_and_ret_lines(os.path.join(data_dir, 'weather_local.txt'))
    lines_src_web = FileUtils.read_file_and_ret_lines(os.path.join(data_dir, 'weather_web.txt'))
    
    for line_local in lines_src_local:
        fields_local = line_local.rstrip('\n').split(',')
        city_id_local = fields_local[0]
        city_name_local = fields_local[1]
        
        logging.info('START ---> match city id %s, city name %s' % (city_id_local, city_name_local))
        flag_id_found = False
        flag_name_found = False

        for line_web in lines_src_web:
            fields_web = line_web.rstrip('\n').split(',')
            city_id_web = fields_web[0]
            city_name_web = fields_web[1]
        
            if city_id_local == city_id_web:
                logging.info('match to web city id %s, city name %s' % (city_id_web, city_name_web))
                flag_id_found = True
                if city_name_local == city_name_web:
                    flag_name_found = True
                break
        # end for
        
        if not flag_id_found:
            g_list_of_city_ids_not_match[city_id_local] = city_name_local
            logging.error('The city id(%s) is NOT match!' % city_name_local)
        if not flag_name_found:
            g_list_of_city_names_not_match[city_id_local] = city_name_local
            logging.error('The city name(%s) is NOT match!' % city_name_local)
        
        logging.info('END ---> match city id %s, city name %s\n' % (city_name_local, city_name_local))
    # end for

def summary_main():
    logging.info('SUMMARY')
    
    logging.info('The list of city ids not matched:')
    if len(g_list_of_city_ids_not_match) > 0:
        for k, v in sorted(g_list_of_city_ids_not_match.items(), key=lambda item:item[0]):
            logging.info('city id: %s, city name: %s' % (k, v))

    logging.info('')
    logging.info('The list of city names not matched:')
    if len(g_list_of_city_names_not_match) > 0:
        for k, v in sorted(g_list_of_city_names_not_match.items(), key=lambda item:item[0]):
            logging.info('city id: %s, city name: %s' % (k, v))

    logging.info('SUMMARY END')


if __name__ == '__main__':

    log_file_path = os.path.join(os.getcwd(), 'log', 'city_list_diff.log')
    LogUtils.init_log_config(logging.DEBUG, logging.INFO, log_file_path)
    diff_main()
    summary_main()
    
    print '%s DONE!' % (os.path.basename(__file__))
