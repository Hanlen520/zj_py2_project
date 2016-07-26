# -*- coding: utf-8 -*-

'''
Created on 2016-7-26

@author: zhengjin

Include the log functions for logging package.

'''

import os
import logging

# ----------------------------------------------------
# Log functions
# ----------------------------------------------------
def init_log_config(main_log_level, file_log_level, file_path):
    long_format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s'
    short_format = '%(filename)s: [%(levelname)s] >>> %(message)s'
    
    long_date_format = '%a, %d %b %Y %H:%M:%S'
    short_date_format = '%d %b %H:%M:%S'

    # log main handler
    logging.basicConfig(level=main_log_level,format=short_format,datefmt=short_date_format)

    # set the file handler
    log_file = logging.FileHandler(filename=file_path, mode='w')
    log_file.setLevel(file_log_level)
    log_file.setFormatter(logging.Formatter(fmt=long_format,datefmt=long_date_format))
    logging.getLogger('').addHandler(log_file)


# ----------------------------------------------------
# Main
# ----------------------------------------------------
if __name__ == '__main__':

    print '%s DONE!' %(os.path.basename(__file__))
    pass
