# -*- coding: utf-8 -*-
'''
Created on 2016-3-3

@author: zhengjin
'''

# ----------------------------------------------------
# Functions
# ----------------------------------------------------
def read_2_list_files():
    # read 2 files
    try:
        f1 = open(path1, 'r')
        list1_records = f1.readlines()
    finally:
        f1.close()

    try:
        f2 = open(path2, 'r')
        list2_records = f2.readlines()
    finally:
        f2.close()

    return list1_records, list2_records
    
def diff_compare(list1_records, list2_records):
    same_list = []
    diff_list = []

    # diff compare
    for item2 in list2_records:
        matched = False
        for item1 in list1_records:
            if (item1.strip('\n').strip() == item2.strip('\n').strip()):
                same_list.append(item2)
                matched = True
        if matched:
            continue
        else:
            diff_list.append(item2)

    return same_list, diff_list

def write_output(same_list, diff_list):
    try:
        f = open(output, 'a')
        f.write('Same list %d: \n' % (len(same_list)))
        f.writelines(same_list)
        f.write('\r\n')
        
        f.write('Diff list %d: \n' % (len(diff_list)))
        f.writelines(diff_list)
    finally:
        f.close()

def records_diff():
    list1_records, list2_records = read_2_list_files()
    same_list, diff_list = diff_compare(sorted(list1_records), sorted(list2_records))
    write_output(same_list, diff_list)


# ----------------------------------------------------
# Main
# ----------------------------------------------------
if __name__ == '__main__':
    
    # set input file format as 'UTF-8 without BOM' for compare in Notepad++
    path1 = r'd:\music_list1.txt'
    path2 = r'd:\music_list2.txt'
    output = r'd:\music_diff_output1.txt'
    records_diff()

    print 'Diff compare DONE!'
