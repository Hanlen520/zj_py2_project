# -*- coding: utf-8 -*-

'''
Created on 2016-7-12

@author: zhengjin
'''

# import os
import unittest
import logging

from ZJPyDemos import PyDemo03

def init_log():

    long_format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
    short_format = '%(filename)-12s: %(levelname)-8s %(message)s'
    
    long_date_format = '%a, %d %b %Y %H:%M:%S'
    short_date_format = '%d %b %H:%M:%S'

    # log main handler
    logging.basicConfig(level=logging.DEBUG, format=short_format, datefmt=short_date_format)

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

class test_multiply(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        logging.debug('method setup.')
        
    def tearDown(self):
        logging.debug('method teardown.')
        unittest.TestCase.tearDown(self)
        
    @classmethod
    def setUpClass(cls):
        super(test_multiply, cls).setUpClass()
        init_log()
        logging.debug('class setup.') 

    @classmethod
    def tearDownClass(cls):
        logging.debug('class teardown.') 
        super(test_multiply, cls).tearDownClass()

    def test_3_x_4(self):
        logging.debug('Verify multiply 3 and 4.')
        self.assertEquals(PyDemo03.multiply(3,4), 12)

    def test_a_x_3(self):
        logging.debug('Verify multiply 3 and a.')
        logging.warn('This test will be failed(失败).')
        self.assertEquals(PyDemo03.multiply(3,'a'), 'aa')

if __name__ == '__main__':

    unittest.main(verbosity=1)

    pass