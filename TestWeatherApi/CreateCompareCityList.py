# -*- coding: utf-8 -*-

'''
Created on 2016-7-22

@author: zhengjin

Get specified cities for weather data compare.
1) main cities
2) first 3 sub cities in area
'''

import os
import re

# ----------------------------------------------------
# Global variables
# ----------------------------------------------------
g_data_dir_path = os.path.join(os.getcwd(), 'data')
g_src_city_list_file_name = 'Weather_city_list.txt'
g_target_city_compare_list_file_name = 'Weather_city_list_compare_test.txt'

g_max_num_cities_of_area_to_add = 3


# ----------------------------------------------------
# IO Functions
# ----------------------------------------------------
def get_city_list_from_src_file(src_city_list_file_path):
    if not os.path.exists(src_city_list_file_path):
        print 'The city list file (%s) is NOT found!' % src_city_list_file_path
        exit(1)
    
    city_list = []
    f = open(src_city_list_file_path, 'r')
    try:
        city_list = f.readlines()
    except Exception, e:
        print 'Exception: %s' % e
        print 'Exception when read lines from source city list file.'
        exit(1)
    finally:
        f.close()

    if len(city_list) == 0:
        print 'Error, read zero record in source city list file!'
        exit(1)

    return city_list

def write_bufferred_lines_into_target_file(target_city_list_file_path, bufferred_lines):
    if os.path.exists(target_city_list_file_path):
        print 'Warn, the target file is exist, and will be over write!'
    
    target_file = open(target_city_list_file_path, 'w')
    try:
        target_file.writelines(bufferred_lines)
        target_file.flush()
    finally:
        target_file.close()
        del bufferred_lines[:]


# ----------------------------------------------------
# Filter Functions
# ----------------------------------------------------
def get_main_city_list(bufferred_lines, city_list):
    print 'Filter main city in the list.'
    
    for position in range(0, len(city_list)):
        city_id = city_list[position].strip().split(',')[0]
        if re.match('1010[1|2|3|4]', city_id):
            bufferred_lines.append(city_list[position])
        else:
            return position

def get_spec_city_list_in_area(bufferred_lines, city_list, start_pos):
    print 'Filter city in the list.'
    num_added = 0
    max_num_to_add = g_max_num_cities_of_area_to_add
    
    for i in range(start_pos, (len(city_list) - 1)):
        city_id = city_list[i].strip().split(',')[0]
        next_city_id = city_list[i + 1].strip().split(',')[0]

        if city_id[3:5] == next_city_id[3:5]:  # same area
            if num_added < max_num_to_add:
                bufferred_lines.append(city_list[i])
                num_added = num_added + 1
            else:
                continue
        else:  # new area
            if num_added < max_num_to_add:
                bufferred_lines.append(city_list[i])
                num_added = 0
            else:
                num_added = 0


# ----------------------------------------------------
# Main
# ----------------------------------------------------
def main():
    # input
    src_file_path = os.path.join(g_data_dir_path, g_src_city_list_file_name)
    city_list = get_city_list_from_src_file(src_file_path)
    
    # filter
    bufferred_lines = []
    position = get_main_city_list(bufferred_lines, city_list)
    bufferred_lines.append('\n')
    get_spec_city_list_in_area(bufferred_lines, city_list, position)
    
    # output
    if len(bufferred_lines) > 0:
        target_file_path = os.path.join(g_data_dir_path, g_target_city_compare_list_file_name)
        write_bufferred_lines_into_target_file(target_file_path, bufferred_lines)
    else:
        print 'Error, the filtered record count in buffer is 0.'


if __name__ == '__main__':
    
    main()
    print '%s Done!' % (os.path.basename(__file__))
