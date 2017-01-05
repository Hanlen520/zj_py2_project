# -*- coding: utf-8 -*-
'''
Created on 2016-7-12

@author: zhengjin
'''

import os
import unittest
import logging

# ------------------------------------------------
# Functions
# ------------------------------------------------
def init_log_config():
    long_format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
    short_format = '%(filename)s: [%(levelname)s] >>> %(message)s'
    
    long_date_format = '%a, %d %b %Y %H:%M:%S'
    short_date_format = '%d %b %H:%M:%S'

    # log main handler
    logging.basicConfig(level=logging.INFO, format=short_format, datefmt=short_date_format)

    # set the console handler
#     console = logging.StreamHandler()
#     console.setLevel(logging.DEBUG)
#     console.setFormatter(logging.Formatter(logging.Formatter(short_format)))
#     logging.getLogger('').addHandler(console)

    # set the file handler
#     log_file = logging.FileHandler(filename=os.path.join(os.getcwd(),'zjunittest.log'),mode='w',encoding='utf-8')
    log_file = logging.FileHandler(filename='zjunittest.log',mode='w')
    log_file.setLevel(logging.WARN)
    log_file.setFormatter(logging.Formatter(fmt=long_format, datefmt=long_date_format))
    logging.getLogger('').addHandler(log_file)

def discover():
    loader = unittest.TestLoader()
    suite1 = loader.discover(start_dir=os.getcwd(),pattern='Unittest*.py')
    all_test = unittest.TestSuite(suite1)
    
    return unittest.TextTestRunner(verbosity=2).run(all_test)


# ------------------------------------------------
# Main
# ------------------------------------------------
if __name__ == '__main__':

    init_log_config()
    discover()

    pass