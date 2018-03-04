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
    log_file = logging.FileHandler(filename='unittest_log.txt', mode='w')
    log_file.setLevel(logging.WARN)
    log_file.setFormatter(logging.Formatter(fmt=long_format, datefmt=long_date_format))
    logging.getLogger('').addHandler(log_file)

def discover():
    loader = unittest.TestLoader()
    test_cases = loader.discover(start_dir=os.getcwd(), pattern='Unittest*.py')
    test_suite = unittest.TestSuite(test_cases)
    return test_suite

def run_with_text_report():
    test_suite = discover()
    test_results = unittest.TextTestRunner(verbosity=2).run(test_suite)
    print '*** Total test cases:', test_results.testsRun
    print '*** Total failed test cases:', len(test_results.failures)

def run_with_html_report():
    import HTMLTestRunner as Runner
    
    report_path = os.path.join(os.getcwd(), "unittest_report.html")
    with open(report_path, "wb") as f:
        runner = Runner.HTMLTestRunner(stream=f, title="ZhengJin Unit Test Demo",
                                       description="Test Cases execution details:") 
        runner.run(discover())
    # end-with


# ------------------------------------------------
# Main
# ------------------------------------------------
if __name__ == '__main__':

    init_log_config()
#     run_with_text_report()
    run_with_html_report()
    print 'unit test execution DONE.'
