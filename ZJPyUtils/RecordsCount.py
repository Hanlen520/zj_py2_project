# -*- coding: utf-8 -*-
'''
Created on 2016-3-15

@author: zhengjin
'''

g_input_f_path = r'd:\music_list2.txt'

def file_readlines(f_path):
    f_list = open(f_path, 'r')
    try:
        lines = f_list.readlines()
    finally:
        f_list.close()
        
    return lines

# get the count for distinct and non-distinct records in file
def get_records_count():
    lines_1 = file_readlines(g_input_f_path)
    lines_2 = file_readlines(g_input_f_path)
    
    distinct_count = 0
    non_distinct_count = 0
    distinct_num = 1
    for line_1 in lines_1:
        record_count = 0
        line_1 = line_1.strip('\n').strip()
        for line_2 in lines_2:
            line_2 = line_2.strip('\n').strip()
            if line_1 == line_2:
                record_count = record_count + 1
        if record_count > distinct_num:
            print 'count --> %d, line --> %s' %(record_count, line_1)
            non_distinct_count = non_distinct_count + 1
        else:
            print 'distinct line --> %s' %(line_1)
            distinct_count = distinct_count + 1
    
    lines_1 = None
    lines_2 = None

    print 'distinct count --> %d' %(distinct_count)
    print 'non distinct count --> %d' %(non_distinct_count)


if __name__ == '__main__':
    get_records_count()
    print 'same records count DONE!'
    pass