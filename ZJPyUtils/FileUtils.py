# -*- coding: utf-8 -*-

'''
Created on 2016-7-20

@author: Vieira

Include the functions for file IO.

'''

import os
import time
import logging
import codecs

# ----------------------------------------------------
# Constants
# ----------------------------------------------------
CHARSET_UTF8 = 'utf-8'
CHARSET_GBK = 'gbk'


# ----------------------------------------------------
# Read functions
# ----------------------------------------------------
def read_file_and_ret_lines(file_path):
    if not os.path.exists(file_path):
        logging.error('The file(%s) to be read is NOT exist!' %file_path)
        return
    
    lines = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
    if len(lines) == 0:
        logging.warn('The file(%s) content is empty.' %file_path)

    return lines

def read_file_and_ret_content(file_path):
    if not os.path.exists(file_path):
        logging.error('The file(%s) to be read is NOT exist!' %file_path)
        return
    
    content = ''
    with open(file_path, 'r') as f:
        content = f.read()
    if len(content) == 0:
        logging.warn('The file(%s) content is empty.' %file_path)

    return content


# ----------------------------------------------------
# Write functions
# ----------------------------------------------------
def write_lines_to_file(file_path, lines, flag_override=True, charset=''):
    if len(lines) == 0:
        logging.error('The length of input lines is 0!')
        return
    
    if os.path.exists(file_path):
        if flag_override:
            logging.info('The file(%s) is exist, and the content will be override!' %file_path)
        else:
            logging.error('The file(%s) is exist!' %file_path)
            return

    if charset == '':
        with open(file_path, 'w') as f:
            f.writelines(lines)
    else:
        with codecs.open(file_path, 'w', charset) as f:
            f.writelines(lines)

def write_content_to_file(file_path, content, flag_override=True, charset=''):
    if len(content) == 0:
        logging.error('The input content is empty!')
        return
    
    if os.path.exists(file_path):
        if flag_override:
            logging.info('The file(%s) is exist, and the content will be override!' %file_path)
        else:
            logging.error('The file(%s) is exist!' %file_path)
            return
        
    if charset == '':
        with open(file_path, 'w') as f:
            f.write(content)
    else:
        with codecs.open(file_path, 'w', charset) as f:
            f.write(content)

def append_lines_to_file(file_path, lines, charset=''):
    if len(lines) == 0:
        logging.error('The length of input lines is 0!')
        return
    
    if not os.path.exists(file_path):
        logging.info('The file(%s) is not exist!' %file_path)
    
    if charset == '':
        with open(file_path, 'a') as f:
            f.writelines(lines)
    else:
        with codecs.open(file_path, 'a', charset) as f:
            f.writelines(lines)

def append_content_to_file(file_path, content, charset=''):
    if len(content) == 0:
        logging.error('The input content is empty!')
        return
    
    if not os.path.exists(file_path):
        logging.info('The file(%s) is NOT exist!' %file_path)
    
    if charset == '':
        with open(file_path, 'a') as f:
            f.write(content)
    else:
        with codecs.open(file_path, 'a', charset) as f:
            f.write(content)


# ----------------------------------------------------
# Directory functions
# ----------------------------------------------------
def create_dir(dir_path):
    if os.path.exists(dir_path):
        return
    
    os.makedirs(dir_path)
    time.sleep(0.5)


# ----------------------------------------------------
# Main
# ----------------------------------------------------
def main_test():
    input_lines = read_file_and_ret_lines(r'C:\Users\zhengjin\Desktop\weather_web_src.txt')
    output_lines = []

    for line in input_lines:
        if not line == '\n':
            output_lines.append(line)
        
    write_lines_to_file('C:\Users\zhengjin\Desktop\weather_web.txt', output_lines)


if __name__ == '__main__':

    main_test()

    print '%s DONE!' %(os.path.basename(__file__))
    pass

