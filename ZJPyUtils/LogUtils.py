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
    log_format_long = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s'
    log_format_short = '%(filename)s: [%(levelname)s] >>> %(message)s'
    
    date_format_long = '%a, %d %b %Y %H:%M:%S'
    date_format_short = '%d %b %H:%M:%S'

    # log main handler
    logging.basicConfig(level=main_log_level,format=log_format_short,datefmt=date_format_short)

    # set file handler
    log_file = logging.FileHandler(filename=file_path, mode='w')
    log_file.setLevel(file_log_level)
    log_file.setFormatter(logging.Formatter(fmt=log_format_long,datefmt=date_format_long))
    logging.getLogger('').addHandler(log_file)


# ----------------------------------------------------
# Main
# ----------------------------------------------------
if __name__ == '__main__':

    init_log_config(logging.DEBUG, logging.INFO, r'd:\test_log.txt')
    logging.debug('debug message')
    logging.info('info message')

    print '%s DONE!' %(os.path.basename(__file__))
    pass
