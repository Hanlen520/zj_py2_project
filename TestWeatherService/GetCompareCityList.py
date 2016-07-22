# -*- coding: utf-8 -*-

'''
Created on 2016-7-22

@author: zhengjin
'''

import os
import re

# ----------------------------------------------------
# Global variables
# ----------------------------------------------------
g_scr_city_list_file_name = 'Weather_city_list_test.txt'
g_target_city_compare_list_file_name  = 'Weather_city_list_compare.txt'


# ----------------------------------------------------
# IO Functions
# ----------------------------------------------------
def get_city_list(input_city_list_file_path):
    if not os.path.exists(input_city_list_file_path):
        print 'The city list file (%s) is NOT found!' %input_city_list_file_path
        exit(1)
    
    f = open(input_city_list_file_path, 'r')
    city_list = f.readlines()
    if len(city_list) == 0:
        print 'Read 0 city item in the city list file!'
        exit(1)

    global g_total_num_of_cities
    g_total_num_of_cities = len(city_list)

    return city_list

def open_file_for_write(output_city_list_file_path):
    print 'TODO:'


# ----------------------------------------------------
# Filter Functions
# ----------------------------------------------------
def filter_main_city_list(city_list):
    for position in range(0,len(city_list)):
        city_id = city_list[position].strip().split(',')[0]
        if re.match('1010[1|2|3|4]', city_id):
            print city_list[position].rstrip('\n')
        else:
            return position

def filter_city_list(city_list, start_pos):
    num_added = 0
    max_num_to_add = 3
    
    for i in range(start_pos,(len(city_list)-1)):
        city_id = city_list[i].strip().split(',')[0]
        next_city_id = city_list[i+1].strip().split(',')[0]

        if city_id[3:5] == next_city_id[3:5] and num_added < max_num_to_add:
            print city_list[i].rstrip('\n')
            num_added = num_added + 1
        elif city_id[3:5] == next_city_id[3:5] and num_added >= max_num_to_add:
            continue
        elif city_id[3:5] != next_city_id[3:5] and num_added < max_num_to_add:
            print city_list[i].rstrip('\n')
            print ''
            num_added = 0
        elif city_id[3:5] != next_city_id[3:5] and num_added >= max_num_to_add:
            print ''
            num_added = 0


# ----------------------------------------------------
# Main
# ----------------------------------------------------
if __name__ == '__main__':
    
    city_list = get_city_list()
    position = filter_main_city_list(city_list)
    print ''
    filter_city_list(city_list, position)
    
    print '%s Done!' %(os.path.basename(__file__))
    pass