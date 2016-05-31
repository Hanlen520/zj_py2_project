# -*- coding: utf-8 -*-
'''
Created on 2015-12-3

@author: zhengjin
'''

import os
import time
import shutil

# ----------------------------------------------------
# Functions
# ----------------------------------------------------
def mk_numbers_of_dirs(target_path, num):
    dir_path = target_path
    sub_path = 'pic_test'
    
    if not os.path.exists(dir_path):
        print 'The target directory path (%s) is not exist.' %(dir_path)
        exit()

    sleep_interval = 0.5
    for i in range(0, num):
        mk_dir_path = os.path.join(dir_path, sub_path + str(i))
        os.mkdir(mk_dir_path)
        time.sleep(sleep_interval)
        print 'Make directory (%s) done.' %(mk_dir_path)

    print 'Make number of directories done!'

def copy_files_per_dir(src_path, target_path, pics_of_each_dir):
    target_dir_path = target_path
    src_pic_path = src_path
    l_pics_of_each_dir = pics_of_each_dir
    pics_path = []
    
    for pic in os.listdir(src_pic_path):
        pics_path.append(os.path.join(src_pic_path, pic))
    print '%d pictures to be copied.' %(len(pics_path))
    
    i = 0
    tmp_path = ''
    for dir in os.listdir(target_dir_path):
        tmp_path = os.path.join(target_dir_path, dir)
        for k in range(0, l_pics_of_each_dir): 
#             shutil.copyfile(pics[i], path)   # if use shutil.copyfile(), permission denied
            shutil.copy(pics_path[i], tmp_path)   # use shutil.copy() instead
            print 'Copy file from %s to %s' %(pics_path[i], tmp_path)
            i += 1
            if i > (len(pics_path) - 1):
                print 'Number of pictures copied - > %d' %(i)
                print 'Copy done!'
                return
        # end for
    # end for

    print 'Number of pictures copied - > %d' %(i)

def copy_files_in_dir(src_path, target_path, copied_num):
    if (not os.path.exists(src_path)) or (not os.path.exists(target_path)):
        print 'The src or target path is not exist.'
        exit()

    if copied_num <= 0:
        print 'Copied number must be greater than 1.'
        exit()
        
    l_src_path = src_path
    l_target_path = target_path
    l_copied_num = copied_num

    files = []
    for file in os.listdir(l_src_path):
        files.append(file)

    sleep_interval = 0.5
    for i in range(0, l_copied_num):
        for j in range(0, len(files)):
            src_file_path = '%s\\%s' %(l_src_path, files[j])
            file_name, file_suffix = format_file_name(files[j])
            target_file_path = '%s\\%s_%d.%s' %(l_target_path, file_name, i, file_suffix)
            
            shutil.copy(src_file_path, target_file_path)
            time.sleep(sleep_interval)
            print 'Copy source file(%s) to target file(%s).' %(src_file_path, target_file_path)

    print 'Copied files in directory done!'

def format_file_name(file_path):
    keys = file_path.split('.')
    return keys[0], keys[1]

def copy_numbers_of_file(file_name, file_suffix, copied_num):
    file_path = '%s.%s' %(file_name, file_suffix)
    if not os.path.exists(file_path):
        print 'The source file (%s) is not exist.' %(file_path)
        exit()
        
    sleep_interval = 0.5
    for i in range(1, (copied_num + 1)):
        copied_file_path = '%s_%d.%s' %(file_name, i, file_suffix)
        shutil.copy(file_path, copied_file_path)
        time.sleep(sleep_interval)
        print 'Copied file %s done.' %(copied_file_path)

    print 'Copy repeat files done!'

# ----------------------------------------------------
# Main
# ----------------------------------------------------
def main_copy_numbers_of_file():
    copied_num = 30000
    file_name = r'D:\files_test\Txts_30000+\test'
    file_suffix = 'txt'

    copy_numbers_of_file(file_name, file_suffix, copied_num)

def main_copy_files_per_dir():
    num = 100
    target_path = r'D:\files_test\Pics_2000+_4perdir'
    src_path = r'E:\Files_haier_test\disk_2\JPEG 2000+'
    mk_numbers_of_dirs(target_path, num)

    pics_of_each_dir = 4
    copy_files_per_dir(src_path, target_path, pics_of_each_dir)

def main_copy_files_from_src_to_target_dir():
    src_path = r'D:\files_test\Txts_10000+'
    target_path = r'D:\files_test\Txts_20000+'
    copied_num = 2
    copy_files_in_dir(src_path, target_path, copied_num)


if __name__ == '__main__':

    main_copy_numbers_of_file()
#     main_copy_files_per_dir()
#     main_copy_files_from_src_to_target_dir()


    print '%s done!' %(os.path.basename(__file__))
    pass